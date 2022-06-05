from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='add_placeholder')
def add_placeholder(value, arg):
    return value.as_widget(attrs={'placeholder': arg})
