from django import template

register=template.Library()

# add class attribute to 'label'
@register.filter
def label_with_classes(value,arg):
    return value.label_tag(attrs={'class': arg})

# add class attribute to 'input'
@register.filter
def widget_with_classes(value,arg):
    return value.as_widget(attrs={'class': arg})