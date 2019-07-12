from django import template

register = template.Library()

@register.filter
def customFilter(value):
    value = value.filter(aproved=True)
    return value
