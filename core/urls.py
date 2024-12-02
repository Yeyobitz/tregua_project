from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('nuestra-historia/', views.nuestra_historia, name='nuestra_historia'),
    path('contacto/', views.contacto, name='contacto'),
]
