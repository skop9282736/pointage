from django import template
import datetime

register = template.Library()

@register.filter
def get_type(value):
	isValid = True
	try:
		year,month,day = value.split('-')
		date = datetime.datetime(int(year),int(month),int(day))
	except ValueError :
		is_valid = False
	if is_valid:
		return '1'
	else:
		return '0'