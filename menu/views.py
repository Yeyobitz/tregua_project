from django.shortcuts import render

def menu(request):
    return render(request, 'menu/menu.html')

def nuestros_platos(request):
    return render(request, 'menu/nuestros_platos.html')
