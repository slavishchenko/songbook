from django import template
from django.template.defaultfilters import stringfilter
from django.utils.text import slugify
import unicodedata
import re

register = template.Library()

@register.filter(name='slug')
@stringfilter
def slug(value):
    return slugify(value, allow_unicode=True)


@register.filter(name='is_link')
@stringfilter
def is_link(s):
    match = re.match(r'https://', s)

    if match:
        return True
    else:
        return False


@register.filter(name='is_list')
@stringfilter
def is_list(l):
    if type(l) == list:
        return True
    else:
        return False
