from django.contrib import admin
from django.urls import path, include
from .views import Manage, create, edit

app_name = 'employees'

urlpatterns = [
	path('manage', Manage.as_view(), name='manage'),
	path('create', create, name='create'),
	path('edit/<str:id>', edit, name='edit'),
]