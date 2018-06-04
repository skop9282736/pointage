from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'employees'

router = routers.DefaultRouter()
router.register('salaries', views.SalaryView)
router.register('groups', views.GroupView)

urlpatterns = [
	path('', include(router.urls), name="salary-api"),
	path('manage', views.manage, name="manage"),
	path('salaries/getid/<int:id_salary_finger>', views.get_salary_id, name="manage"),
	path('groups/getid/<int:id>', views.get_group_id, name="manage_group"),
]