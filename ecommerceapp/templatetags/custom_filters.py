from django import template

register = template.Library()

@register.filter  # with için
def mul(value, arg):
    return value * arg

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg