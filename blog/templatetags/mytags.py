from django import template

register = template.Library()

@register.filter
def getall(quert_set):
    return  quert_set.all()
