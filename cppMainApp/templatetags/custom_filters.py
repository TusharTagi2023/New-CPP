from django import template

register = template.Library()

@register.filter(name='dot')
def dot(dictionary):
    return list(dictionary.values())
