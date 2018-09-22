from django.shortcuts import render
from employees.models import GroupSalaries,Salary
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/admin/login/')
def home_page(request):
	context = {
		'nb_group': GroupSalaries.objects.all().count(),
		'nb_salary': Salary.objects.all().count()
	}
	return render(request, 'global/home.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')