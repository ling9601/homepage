from django import template

register = template.Library()

@register.filter
def price2string(price):
    # price /= 1000
    if price:
        return '{:20,d}'.format(int(price))
    else:
        return None
@register.simple_tag
def get_total_num(wanted_item):
    catched_items = wanted_item.catcheditem_set.all()
    return sum([item.store_item.num for item in catched_items])