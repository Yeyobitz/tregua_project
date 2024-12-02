from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm
from .services import ReservationService

def reservas(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            is_available, result = ReservationService.check_table_availability(
                form.cleaned_data['date'],
                form.cleaned_data['time'],
                form.cleaned_data['number_of_people']
            )
            
            if is_available:
                reservation.table = result
                reservation.save()
                messages.success(request, 'Reserva realizada correctamente')
                return redirect('reservations:reservas')
            else:
                messages.error(request, result)
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/reservas.html', {'form': form})