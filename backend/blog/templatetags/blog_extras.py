from ..models import Post, Category, Tag

from django import template
from django.template.defaultfilters import stringfilter
from django.db.models.aggregates import Count

import markdown

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """ get categories with num_posts attach to it """
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    """ get tags with num_posts attach to it """
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.filter
@stringfilter
def to_markdown(value):
    md_text = markdown.markdown(value,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',])
    return md_text