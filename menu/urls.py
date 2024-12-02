from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu, name='menu'),
    path('nuestros-platos/', views.nuestros_platos, name='nuestros_platos'),
]