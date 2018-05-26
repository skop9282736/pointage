from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import View
from .forms import EmployeeForm
from .models import Salary
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
class Manage(View):
	def get(self, request):
		form = EmployeeForm()
		salaries = Salary.objects.order_by('-id')
		context = {
			"form": form,
			'salaries': salaries
		}
		return render(request, 'employees/manage.html', context)


def save_all(request, form, template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['added'] = True
			salaries = Salary.objects.order_by('-id')
			data['salaries'] = render_to_string('employees/components/list-emp.html', {'salaries': salaries})
		else:
			data['added'] = False
	context = {
		'form': form
	}
	data['html_form'] = render_to_string(template_name, context=context, request=request)
	return JsonResponse(data)

def create(request):
	if request.method == 'POST':
		form = EmployeeForm(request.POST)
	else:
		form = EmployeeForm()
	return save_all(request, form, 'employees/components/add-emp.html')

def edit(request, id):
	salary = Salary.objects.filter(id=id).first()
	if request.method == 'POST':
		form = EmployeeForm(request.POST, instance=salary)
	else:
		form = EmployeeForm(instance=salary)
	return save_all(request, form, 'employees/components/edit-emp.html')