
from random import randint
from typing import Any, Dict

from account.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from utils.general import (get_last_n_days, get_total_seconds_from_start,
                           is_ajax)

from .models import FreeRollLink, Message, PromoCode, RollValue, Transaction
from .forms import WithdrawalForm


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'panel/index.html'
    extra_context = {
        'title': ' | Freeomi.com | Start rolling!'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roll_values'] = RollValue.objects\
            .all().order_by('payout_dollar')

        # Calculate remaining time
        now_time = get_total_seconds_from_start()
        last_roll = self.request.user.profile.roll_time
        required_lap_in_seconds = settings.ROLL_SECONDS
        interval = now_time - last_roll
        remaining_time = 0
        if 0 <= interval < required_lap_in_seconds:
            remaining_time = required_lap_in_seconds - interval

        context['remaining_time'] = remaining_time

        return context

    def post(self, request, *args, **kwargs):

        if is_ajax(request):
            now_time = get_total_seconds_from_start()
            last_roll = request.user.profile.roll_time
            required_lap_in_seconds = settings.ROLL_SECONDS
            interval = now_time - last_roll
            if required_lap_in_seconds > interval >= 0:
                data = {
                    'message': 'Not yet time'
                }
                return JsonResponse(data, status=400)

            data = {
                'lucky_number': 0,
                'pending_rolls': 0,
                'remaining_seconds': required_lap_in_seconds,
                'coins_won': 0,
                'total_coins': 0,
            }

            roll = randint(0, 300)
            data['lucky_number'] = roll
            roll_value = RollValue.objects\
                .filter(lucky_number_start__lte=roll)\
                .filter(lucky_number_end__gte=roll).first()
            token_won = roll_value.value_in_omi
            data['coins_won'] = token_won

            request.user.transaction_set.create(
                tx_type='earn',
                credit=True,
                amount=token_won,
            )
            if request.user.transaction_set.count() <= 1:
                data['first'] = True

            data['total_coins'] = request.user.get_balance()

            request.user.profile.roll_time = now_time
            request.user.profile.save()
            return JsonResponse(data, status=200)


@login_required
def view_use_promo_code(request):
    """
    Check if user can use promo code
    and if so, use it
    Returns redirect to the same page if user
    can't use promo code
    """
    if is_ajax(request):
        code = request.POST.get('code')
        promo_code = PromoCode.objects.filter(code=code)\
            .filter(valid_until__gte=timezone.now()).first()
        if promo_code and \
            not request.user.profile.has_used_promo_code(
                promo_code):
            request.user.profile.use_promo_code(promo_code)
            data = {
                'message': 'Promo code applied, roll again!'
            }
            return JsonResponse(data, status=200)

    data = {
        'message': 'Promo code is not valid, expired or already used'
    }
    return JsonResponse(data, status=400)


class Withdraw(LoginRequiredMixin, TemplateView):
    template_name = 'panel/withdrawal.html'
    extra_context = {
        'title': ' | Withdrawals'
    }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['withdrawals'] = self.request.user.withdrawalrequest_set.all()
        return context

    def post(self, request, *args, **kwargs):
        form = WithdrawalForm(data=request.POST, initial={
            "user": self.request.user
        })

        if form.is_valid():
            form.save()
            messages.success(
                request, "Withdrawal request sent, \
will be completed in a few days. You can check your withdrawal requests in \
`My Withdrawal` tab below.")
            return redirect("panel:withdrawal")

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class Stats(LoginRequiredMixin, TemplateView):
    template_name = 'panel/stats.html'
    extra_context = {
        'title': ' | Statistics'
    }

    def format_last_days(self):
        return [
            day.strftime("%d %b, %Y")
            for day in
            self.last_days
        ]

    def get_ecomi_won_analysis(self):
        values = [
            self.token_queryset.get_earned().date_sum_amount(date)
            for date in
            self.last_days
        ]

        template = [
            {
                "date": date,
                "value": value
            }
            for date, value in
            zip(self.last_days_format, values)
        ]

        analysis = {
            "name": f"Ecomi won in the last {len(self.last_days)} days",
            "dates": self.last_days_format,
            "values": values,
            "template": template
        }
        return analysis

    def get_referral_analysis(self):
        values = [
            self.token_queryset.get_referrals().date_sum_amount(date)
            for date in
            self.last_days
        ]

        template = [
            {
                "date": date,
                "value": value
            }
            for date, value in
            zip(self.last_days_format, values)
        ]

        analysis = {
            "name": f"Referral commission earned in \
last {len(self.last_days)} days",
            "dates": self.last_days_format,
            "values": values,
            "template": template
        }
        return analysis

    def get_payment_analysis(self):
        values = [
            self.token_queryset.get_payments().date_sum_amount(date)
            for date in
            self.last_days
        ]

        template = [
            {
                "date": date,
                "value": value
            }
            for date, value in
            zip(self.last_days_format, values)
        ]

        analysis = {
            "name": f"Payments sent in \
last {len(self.last_days)} days",
            "dates": self.last_days_format,
            "values": values,
            "template": template
        }
        return analysis

    def get_users_analysis(self):
        addition = timezone.timedelta(days=1)
        values = [
            User.objects.filter(
                created__gte=date
            ).filter(
                created__lt=(date + addition)
            ).count()
            for date in
            self.last_days
        ]

        template = [
            {
                "date": date,
                "value": value
            }
            for date, value in
            zip(self.last_days_format, values)
        ]

        analysis = {
            "name": f"User registration in \
last {len(self.last_days)} days",
            "dates": self.last_days_format,
            "values": values,
            "template": template
        }
        return analysis

    def get_token_analysis(self):
        values = [
            self.token_queryset.get_earned().date_sum_amount(date)
            for date in
            self.last_days
        ]

        template = [
            {
                "date": date,
                "value": value
            }
            for date, value in
            zip(self.last_days_format, values)
        ]

        analysis = {
            "name": f"Tokens earned in \
last {len(self.last_days)} days",
            "dates": self.last_days_format,
            "values": values,
            "template": template
        }
        return analysis

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.token_queryset = Transaction.objects.all()
        self.last_days = get_last_n_days(10)
        self.last_days_format = self.format_last_days()

        context["analysis"] = {
            "ecomi_won": self.get_ecomi_won_analysis(),
            "referral_commission": self.get_referral_analysis(),
            "payments_sent": self.get_payment_analysis(),
            "users_registered": self.get_users_analysis(),
            "token_won": self.get_token_analysis(),
        }

        return context


class Referral(LoginRequiredMixin, TemplateView):
    template_name = 'panel/referral.html'
    extra_context = {
        'title': ' | Referral Program'
    }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['site'] = get_current_site(self.request).domain
        context['total_earned'] = self.request.user.total_earned_referral()
        context['recent_earned'] = self.request.user.recent_earned_referral()
        return context


class FreeRollsView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/free-rolls.html'
    extra_context = {
        'title': ' | Get Free Rolls'
    }

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['lifetime'] = round(settings.ROLL_LINK_LIFETIME / 60 / 60)
        context['freebitcoin_links'] = FreeRollLink.objects.all()
        return context


@login_required
def use_free_roll_link(request, link_id):
    link = FreeRollLink.objects.filter(id=link_id).first()
    if link:
        user = request.user
        if user.can_use_roll_link(link):
            user.use_roll_link(link)
            messages.success(
                request, 'You have successfully used a free roll link')
            return redirect(link.url)
    messages.warning(request, 'Link used or expired')
    return redirect('panel:free_rolls')


class Messages(LoginRequiredMixin, ListView):
    template_name = 'panel/messages.html'
    extra_context = {
        'title': ' | Messages'
    }
    model = Message
    context_object_name = 'messages_posts'
    ordering = '-created'


class MessageDetail(LoginRequiredMixin, DetailView):
    template_name = 'panel/message-detail.html'
    model = Message
    context_object_name = 'message'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' | Messages | ' + self.get_object().title
        return context


class EarnMorePage(LoginRequiredMixin, TemplateView):
    template_name = 'panel/earn_more.html'
    extra_context = {
        'title': ' | Earn More',
        'tokens_per_usd': settings.TOKEN_PER_USD,
        'min_withdraw': settings.MIN_TOKEN_REDEEMABLE,
    }

    mapping = {
        'bitlab': 'panel/tokens/bitlab.html',
        'cpx': 'panel/tokens/cpx.html',
        'timewall': 'panel/tokens/timewall.html',
    }

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            tab = request.POST.get('tab')
            template = self.mapping[tab]
            content = render_to_string(
                template,
                context={
                    'user_id': request.user.profile.uid,
                    'bitlab_token': settings.BITLAB_TOKEN,
                    'email': request.user.email,
                    'app_id': settings.CPX_APP_ID,
                }
            )
            return JsonResponse({'content': content})
        return super().get(request, *args, **kwargs)


class ErrorException(Exception):
    pass


@login_required
def redeem_tokens(request):
    """Redeem amount of tokens"""
    try:
        if is_ajax(request):
            amount = float(request.POST.get('amount') or 0)

            if amount < settings.MIN_TOKEN_REDEEMABLE:
                raise ErrorException(
                    f'Minimum amount is {settings.MIN_TOKEN_REDEEMABLE}')

            if amount > float(request.user.get_token_balance()):
                raise ErrorException('You do not have enough tokens')

            request.user.surveytoken_set.redeem_tokens(
                request.user, amount)
            return JsonResponse({
                'message': f"You have successfully redeemed {amount} tokens"
            })

    except ErrorException as e:
        return JsonResponse({
            'message': str(e)
        }, status=400)

    return JsonResponse(status=400)
