from django.contrib import admin
from django.urls import path, include
from .views import home_page, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('employees/', include('employees.urls', namespace='employees')),
    path('pointage/', include('pointage.urls', namespace='pointage')),
    path('logout/', logout_view, name="logout")
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
