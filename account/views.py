
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView

from utils.general import remove_session, verify_next_link

from .forms import (ChangeEmailForm, ChangePasswordForm, ForgetPasswordForm,
                    LoginForm, UserRegisterForm, WithdrawalForm)
from .models import Profile, User
from .tokens import acount_confirm_token


@login_required
def export(request):
    """Export users usernames and emails"""
    if request.user.is_admin:

        users = User.objects.all()
        result = "username, email\n"
        for user in users:
            line = f"{user.profile.username}, {user.email}\n"
            result += line

        response = HttpResponse(result.encode('ascii'), content_type='csv')
        response['Content-Disposition'] = "attachment; filename=users.csv"
        return response

    return redirect("panel:index")


def verification_message(request, user, template):
    site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = acount_confirm_token.make_token(user)

    name = user.profile.username

    message = render_to_string(template, {
        "user": name,
        "uid": uid,
        "token": token,
        "domain": site.domain,
        'from': settings.DEFAULT_FROM_EMAIL
    })
    return message


def send_activation_email(request, user):
    subject = "Freeomi Email Verification"
    message = verification_message(
        request, user, "account/email.html")
    user.email_user(subject, message)


def activate_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        # Check if the user is already verified
        if user.verified:
            messages.success(request, 'Email is already verified')

        # Check if the token is valid
        elif acount_confirm_token.check_token(user, token):
            user.verified = True
            user.save()

            # Login user automatically
            login(request, user)

            messages.success(
                request,
                'Your account is successfully verified. \
You are automatically logged in, start rolling!.')
            return redirect(reverse('panel:index'))

        else:
            # Send another verification email
            send_activation_email(request, user)

            messages.success(
                request, 'Email verification link has expired or invalid, \
                    Another verification email has been sent to you. Give \
                        it a few minutes, and don\'t forget to check your \
                            spam folder.')
    else:
        messages.warning(request, 'Invalid verification link.')

    return redirect('landing:landing')


@login_required
def resend_activation_link(request):
    subject = "Freeomi Email Verification"
    message = verification_message(
        request, request.user, "account/email.html")
    request.user.email_user(subject, message)
    messages.success(
        request, 'A New verification email has been sent to you. Give \
                it a few minutes, and don\'t forget to check your \
                    spam folder.')
    return redirect(reverse("panel:index"))


def login_account(request):
    # Initialize data
    form = LoginForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)

            # Get next link
            next = verify_next_link(request.POST.get('next'))
            next = next if next else reverse('panel:index')
            return JsonResponse({'redirect': next}, status=200)

        else:
            return JsonResponse(
                {'email': 'Account has been disabled'}, status=400)

    return JsonResponse(form.errors, status=400)


def forget_password(request):
    # Initialize data
    form = ForgetPasswordForm(data=request.POST)

    if form.is_valid():
        form.save()
        messages.success(
            request,
            'Your password has been changed successfully!')
        return JsonResponse(
            {'redirect': reverse('landing:landing')}, status=200)

    return JsonResponse(form.errors, status=400)


def register_account(request):
    # Initialize data
    form = UserRegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()

        # Check if there is a referrer
        ref = request.session.get('ref')
        if ref:
            try:
                referrer = Profile.objects.get(code=ref)
                user.profile.referrer = referrer.user
                user.profile.save()

                # Delete ref session key
                remove_session(request, 'ref')

            except Profile.DoesNotExist:
                pass

        # Login user automatically
        login(request, user)

        # Send verification link
        send_activation_email(request, user)

        messages.success(
            request,
            'Your account is successfully created.\
You are automatically logged in, start rolling!.')
        return JsonResponse({'redirect': reverse('panel:index')}, status=200)

    return JsonResponse(form.errors, status=400)


class Settings(LoginRequiredMixin, TemplateView):
    template_name = 'account/settings.html'
    extra_context = {
        'title': ' | Settings'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['withdrawal_form'] = WithdrawalForm(
            instance=self.request.user.profile)
        context['email_form'] = ChangeEmailForm(instance=self.request.user)
        context['password_form'] = ChangePasswordForm(
            instance=self.request.user)
        context['step'] = 'withdrawal'

        return context

    def post(self, request, *args, **kwargs):
        step = request.POST.get('step')
        context = self.get_context_data()
        context['step'] = step

        if step == 'withdrawal':
            form = WithdrawalForm(
                instance=self.request.user.profile, data=request.POST)

            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Withdrawal address is successfully updated')
                return redirect('account:settings')

            context['withdrawal_form'] = form
        elif step == 'email':
            form = ChangeEmailForm(
                instance=self.request.user, data=request.POST)

            if form.is_valid():
                form.save()

                messages.success(
                    request, 'Email address is successfully updated')
                return redirect('account:settings')

            context['email_form'] = form
        else:
            # For change password
            form = ChangePasswordForm(
                instance=self.request.user, data=request.POST)

            if form.is_valid():
                form.save()

                messages.success(
                    request,
                    'Password is successfully updated,\
now login with new password!')

                return redirect('landing:landing')

            context['password_form'] = form

        return render(request, self.template_name, context)


def Logout(request):
    logout(request)
    return redirect('landing:landing')
