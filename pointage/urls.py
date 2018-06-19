from django.urls import path, include
from .views import profile, reports,manage
from . import views
from rest_framework import routers
from employees.views import GroupView 
app_name = 'pointage'
router = routers.DefaultRouter()
router.register('times', views.TimeEnterView)
router.register('groups', GroupView)
urlpatterns = [
    path('profile/<int:id>', profile, name="profile"),
    path('', include(router.urls), name="TimeEnter-api"),
    path('reports', reports, name="reports"),
    path('gerer_tempe/', manage, name="gererTempe"),
    path('times/getid/<int:id>', views.get_time_id, name="get_id_time"),
]
