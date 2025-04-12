from django import template
import math

register = template.Library()


@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ""


@register.filter
def floor_int(value):
    try:
        return int(math.floor(float(value)))
    except (ValueError, TypeError):
        return 0
