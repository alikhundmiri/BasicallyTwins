from django import template

register = template.Library()

@register.filter
def show_last_string(value, length=3):
    return ('*'*len(value[:-length])+value[-length:])
