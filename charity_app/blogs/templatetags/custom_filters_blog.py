from django import template

register = template.Library()


@register.filter
def break_loop(value, index):
    return value[:index]
