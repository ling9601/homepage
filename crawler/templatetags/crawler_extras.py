from django import template

register = template.Library()

@register.filter
def price2string(price):
    # price /= 1000
    if price:
        return '{:20,d}'.format(int(price))
    else:
        return None