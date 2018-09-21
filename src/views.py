from django.shortcuts import render
from employees.models import GroupSalaries,Salary

# Create your views here.

def home_page(request):
	context = {
		'nb_group': GroupSalaries.objects.all().count(),
		'nb_salary': Salary.objects.all().count()
	}
	return render(request, 'global/home.html', context)
