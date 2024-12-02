from django.shortcuts import render

def nuestra_historia(request):
    return render(request, 'core/nuestra_historia.html')

def contacto(request):
    return render(request, 'core/contacto.html')