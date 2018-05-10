import json as json_lib

from django import template

register = template.Library()


@register.filter
def json(value):
    return json_lib.dumps(value)
