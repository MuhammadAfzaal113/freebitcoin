import datetime
import re
import socket

from bs4 import BeautifulSoup
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError  # noqa
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string

from .logger import err_logger, logger  # noqa


def parse_html_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.text


def parse_first_image(html):
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find('img')
    if img:
        return img.attrs.get('src')
    return "https://cryptoslate.com/wp-content/uploads/2021/03/ecomi-social.jpg"


def invalid_str(value):
    # This checks if a string contains special chars or not
    for i in '@#$%^&*+=://;?><}{[]()':
        if i in value:
            return True
    return False


# Get if a request is an ajax request
def is_ajax(request):
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT'))
    return not requested_html


def get_total_seconds_from_start():
    """
    Code to get total seconds from 1970 till now
    """

    now = datetime.datetime.now()
    td = (now-datetime.datetime(1970, 1, 1))
    return td.total_seconds()


def choices_to_dict(dicts=None):
    if dicts is None:
        dicts = {}
    return [{'value': a[0], 'name': a[1]} for a in dicts]


# Print that only works when on
def printt(*args, **kwargs):
    if settings.PRINT_LOG:
        return print(*args, **kwargs)


def send_email(email, subject, message, fail=True):
    if settings.DEBUG is True:
        print(message)

    if settings.OFF_EMAIL:
        return True

    val = send_mail(
        subject=subject, message=message,
        html_message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email], fail_silently=fail)

    return True if val else False


# Code to remover session if it exists
def remove_session(request, name):
    session = request.session.get(name, None)
    if session is not None:
        del request.session[name]


def verify_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        pass
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if verify_ip(ip):
        return ip


def verify_next_link(next):
    if next:
        if next.startswith('/'):
            return next


def get_next_link(request):
    next = request.GET.get('next')
    return verify_next_link(next)


def decamelize(text):
    if text:
        texts = text.split('_')
        texts = [i.capitalize() for i in texts]
        return ' '.join(texts)

    return ''


def add_queryset(a, b):
    return a | b


# Get value of token in dollars
def get_token_value():
    val = cache.get('token_price')

    if val is None:
        val = token_current_price('OMI')
        cache.set('token_price', val, (60 * 60))

    return val


def convert_dollar_to_token(dollar: float):
    token_price = get_token_value()
    return dollar / token_price


def convert_token_to_dollar(token: float):
    token_price = get_token_value()
    return token * token_price


def get_random_code(obj, rand_str=None):
    if rand_str is None:
        rand_str = get_random_string(length=10)

    exists = obj.__class__.objects.filter(code=rand_str).exists()

    if exists:
        return get_random_code(obj)

    return rand_str


def token_current_price(token_symbol):
    try:
        cmc = CoinMarketCapAPI(settings.COINMARKET_API_KEY)

        r = cmc.cryptocurrency_info(symbol=token_symbol)

        descs = r.data[token_symbol]['description'].split(' ')
        for a, b in enumerate(descs):
            if b == 'USD':
                try:
                    price = float(descs[a-1].replace(',', ''))
                except Exception:
                    price = 0.001

                break

        return price
    except Exception:
        return 0.001


def get_last_n_days(n: int):
    today = timezone.now()
    today = today - timezone.timedelta(
        hours=today.hour,
        minutes=today.minute,
        seconds=today.second,
        microseconds=today.microsecond,
    )
    last_n_days = [today]
    reducer = timezone.timedelta(days=1)
    for _ in range(n-1):
        today = today - reducer
        last_n_days.append(today)
    return last_n_days


def gen_last_n_days(n: int):
    today = timezone.now()
    yield today

    reducer = timezone.timedelta(days=1)
    for _ in range(n-1):
        today = today - reducer
        yield today
