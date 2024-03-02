from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def request_scheme_and_host(context):
    request = context['request']
    return request.scheme + '://' + request.get_host()
