from django import template 

register = template.Library()

@register.inclusion_tag('account/translate.html')
def google_translate(type="simple",language="en"):
    return {
        "language":language,
        "type":type
    }