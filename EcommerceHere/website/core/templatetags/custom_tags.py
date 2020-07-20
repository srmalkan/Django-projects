from django import template
from django.urls import reverse

register = template.Library()

@register.filter('input_type')
def input_type(ob):
    return ob.field.widget.__class__.__name__


@register.filter(name='add_classes')
def add_classes(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    return value.as_widget(attrs={'class': ' '.join(css_classes)})

@register.filter
def cart_count(user):
    if user.is_authenticated:
        orders = user.orders.all().filter(ordered=False)
        if orders.exists():
            order=orders[0]
            return order.items.count()
        
    return 0