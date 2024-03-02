from account.models import User
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from panel.models import Post, Transaction, SurveyToken
from .utils import sha1_hash, compare_digest, md5_hash


class Index(TemplateView):
    template_name = 'landing/index.html'
    extra_context = {
        'title': ' | Free OMI Digital Currency | Freeomi.com',
        'homepage': True,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_key'] = settings.HCAPTCHA_SITEKEY

        # Calculate stats
        earning_set = Transaction.objects.get_earned()
        context['stat_users'] = User.objects.count()
        context['stat_games'] = earning_set.count()
        context['stat_earns'] = round(earning_set.sum_amount(), 4)

        return context

    def get(self, request, *args, **kwargs):
        ref = request.GET.get('ref')
        if ref:
            request.session['ref'] = ref
            return redirect('landing:landing')

        if request.user.is_authenticated:
            return redirect('panel:index')

        return super().get(request, *args, **kwargs)


class GDPR(TemplateView):
    template_name = 'landing/gdpr.html'
    extra_context = {
        'title': ' | GDPR'
    }


class Faq(TemplateView):
    template_name = 'landing/faq.html'
    extra_context = {
        'title': ' | Frequently Asked Question'
    }


class Blog(ListView):
    template_name = 'landing/blog.html'
    extra_context = {
        'title': ' | Blog'
    }
    model = Post
    context_object_name = 'posts'
    ordering = '-updated'


class BlogDetailPage(DetailView):
    template_name = 'landing/blog-detail.html'
    model = Post
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' | Blog | ' + self.get_object().title
        return context


# Survey callbacks
@csrf_exempt
def bitlab_callback(request):
    """
    Callback for receiving bitlab request

    Sample request:
    https://freeomi.com/bitlab/?uid=8cc877ee-af19-488d-b28d-216fb866b996
    &val=4.52&tx=104782
    &hash=dbcd6bb8ca677344592842a52b4fca9bec36cd4b
    """

    url = request.path_info
    uid = request.GET.get('uid')
    val = request.GET.get('val')
    tx = request.GET.get('tx')
    hash = request.GET.get('hash')
    if not uid or not val or not hash:
        return HttpResponseBadRequest('Invalid request')

    # Check hash
    msg = f"https://freeomi.com{url}?uid={uid}&val={val}&tx={tx}"
    if not compare_digest(hash, sha1_hash(msg, settings.BITLAB)):
        return HttpResponseBadRequest('Invalid request')

    try:
        SurveyToken.objects.add_survey_transaction(uid, val, tx)
    except Exception:
        return HttpResponseBadRequest('Invalid request')

    return HttpResponse('OK')


@csrf_exempt
def cpx_callback(request):
    """
    Callback for receiving cpx request

    Sample request:
    https://www.freeomi.com/cpx/?status={status}
    &trans_id={trans_id}&user_id={user_id}
    &amount_local={amount_local}&hash={secure_hash}
    """

    user_id = request.GET.get('user_id')
    trans_id = request.GET.get('trans_id')
    status = request.GET.get('status')
    amount_local = request.GET.get('amount_local')
    hash = request.GET.get('hash')

    # Check hash
    msg = f"{user_id}-{settings.CPX_HASH}"
    if not compare_digest(hash, md5_hash(msg)):
        return HttpResponseBadRequest('Invalid request')

    try:
        if status == '1':
            SurveyToken.objects.add_survey_transaction(
                user_id, amount_local, trans_id)
        else:
            # Delete failed transaction
            tx = SurveyToken.objects.get(txid=trans_id)
            tx.delete()

    except Exception:
        return HttpResponseBadRequest('Invalid request')

    return HttpResponse('OK')
