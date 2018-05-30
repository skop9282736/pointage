from django.urls import path
from .views import profile

app_name = 'templates'

urlpatterns = [
    path('profile/<int:id>', profile, name="profile"),
]
