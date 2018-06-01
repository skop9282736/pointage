from django.shortcuts import render, get_object_or_404
from employees.models import Salary
from .models import Summary, TimeEnter
from .pointages import show_pointages

# Create your views here.
def profile(request, *args, **kwargs):
	salary 		= get_object_or_404(Salary, id_salary_finger = kwargs['id'])
	summary 	= None
	new_list 	= ''
	legal_time 	= get_object_or_404(TimeEnter, group=salary.group_salary)

	if request.method == 'POST':
		new_list 	= show_pointages(request.POST.get('start'), request.POST.get('end'),salary, Summary, legal_time)

	context = {
		'salary' : salary,
		'summary': summary,
		'dates' : new_list,
		'legal_time': legal_time
	}
	return render(request, 'pointage/employees/profile.html', context)