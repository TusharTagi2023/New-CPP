from django import template

register = template.Library()

@register.filter(name='dictValueToList')
def dictValueToList(data):
    return list(data.values())