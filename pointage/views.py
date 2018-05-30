from django.shortcuts import render, get_object_or_404
from employees.models import Salary
from .models import Summary
from .pointages import show_pointages

# Create your views here.
def profile(request, *args, **kwargs):
	salary = get_object_or_404(Salary, id_salary_finger = kwargs['id'])
	summary = None
	if request.method == 'POST':
		new_list 	= show_pointages(request.POST.get('start'), request.POST.get('end'),salary, Summary)

	context = {
		'salary' : salary,
		'summary': summary,
		'dates' : new_list
	}
	return render(request, 'pointage/employees/profile.html', context)