from django.shortcuts import render, get_object_or_404
from employees.models import Salary, GroupSalaries
from .models import Summary, TimeEnter
from .pointages import show_pointages

# Create your views here.
def profile(request, *args, **kwargs):
	salary 		= get_object_or_404(Salary, id_salary_finger = kwargs['id'])
	new_list 	= []
	# group = get_object_or_404(GroupSalaries, salary.group)
	legal_time 	= get_object_or_404(TimeEnter, group=salary.group_salary)

	if request.method == 'POST':
		new_list 	= show_pointages(request.POST.get('start'), request.POST.get('end'),salary, Summary, legal_time)

	context = {
		'salary' : salary,
		'dates' : new_list,
		'legal_time': legal_time
	}
	return render(request, 'pointage/employees/profile.html', context)


def reports(request):
	salaries = Salary.objects.all()
	new_list = []

	if request.method == 'POST':
		for salary in salaries:
			legal_time 	= get_object_or_404(TimeEnter, group=salary.group_salary)
			new_list += [["{} {}".format(salary.first_name, salary.last_name), '0']]
			new_list += [show_pointages(request.POST.get('start'), request.POST.get('end'),salary, Summary, legal_time)]	

	context = {
		'dates' : new_list,
	}
	return render(request, 'pointage/employees/reports.html', context)
