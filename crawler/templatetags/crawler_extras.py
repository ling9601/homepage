from django import template

register = template.Library()

@register.filter
def price2string(price):
    return '{:20,f} Z'.format(price)