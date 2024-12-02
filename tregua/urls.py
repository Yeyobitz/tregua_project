from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('core.urls')),
    path('menu/', include('menu.urls')),
    path('reservas/', include('reservations.urls')),
]
