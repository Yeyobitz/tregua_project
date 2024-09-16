# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('reservas/', views.reservas, name='reservas'),
    path('contacto/', views.contacto, name='contacto'),
    path('nuestra_historia/', views.nuestra_historia, name='nuestra_historia'),
    path('nuestros_platos/', views.nuestros_platos, name='nuestros_platos'),
]
