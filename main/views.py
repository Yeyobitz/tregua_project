from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def menu(request):
    return render(request, 'main/menu.html')

def reservas(request):
    return render(request, 'main/reservas.html')

def contacto(request):
    return render(request, 'main/contacto.html')

def nuestra_historia(request):
    return render(request, 'main/nuestra_historia.html')

def nuestros_platos(request):
    return render(request, 'main/nuestros_platos.html')