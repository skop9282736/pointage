from django import template
import math


register = template.Library()

@register.filter
def check_pointage(value):
    pass