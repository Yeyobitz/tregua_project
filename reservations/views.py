from django.shortcuts import render

def reservas(request):
    return render(request, 'reservations/reservas.html')
