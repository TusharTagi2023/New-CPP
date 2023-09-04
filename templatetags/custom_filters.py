from django import template

register = template.Library()



@register.filter(name='do')
def do(data,key=None):
    print (list(data.values()))
    return 666