from django import template
from utils.general import get_token_value

register = template.Library()


@register.simple_tag()
def get_omi_price():
    return get_token_value()


@register.simple_tag()
def has_used_link(user, link):
    if not user.can_use_roll_link(link):
        return 'active'
