from django import template

register=template.Library()

@register.filter
def BytesToMB(size):
    return size/pow(2,20)