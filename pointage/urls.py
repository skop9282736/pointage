from django.urls import path
from .views import profile, reports

app_name = 'pointage'

urlpatterns = [
    path('profile/<int:id>', profile, name="profile"),
    path('reports', reports, name="reports"),
]
