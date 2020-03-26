from django import template
from django.db.models.aggregates import Count

from ..models import Category, Tag
from users.models import User

register = template.Library()


@register.filter
def BytesToMB(size):
    return size/pow(2, 20)


@register.simple_tag
def get_categories():
    """ get categories with num_images attach to it """
    return Category.objects.annotate(num_images=Count('image')).filter(num_images__gt=0)


@register.simple_tag
def get_tags():
    """ get tags with num_images attach to it """
    return Tag.objects.annotate(num_images=Count('image')).filter(num_images__gt=0)


@register.simple_tag
def get_uploaders():
    """ get tags with num_images attach to it """
    return User.objects.annotate(num_images=Count('image')).filter(num_images__gt=0)
