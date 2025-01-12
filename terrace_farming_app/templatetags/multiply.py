from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(a,b):
    return int(a) * int(b)