import urllib
from django import template

register = template.Library()


@register.filter
def cssescape(value):
    return value.replace('\\', '\\\\').replace("'", "\'").replace('"', '\"')


@register.filter
def googleencode(value):
    return urllib.quote_plus(value)
