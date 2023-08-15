from django import template

register = template.Library()


@register.filter
def placeholder(input_field, text):
    input_field.field.widget.attrs['placeholder'] = text
    return input_field


@register.filter
def form_field_class(form_field, text):
    default_classname = form_field.field.widget.attrs.get('class', '')
    form_field.field.widget.attrs['class'] = default_classname + ' ' + text
    return form_field
