from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm
from .services import ReservationService

def reservas(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.notification_preference = request.POST.get('notification_preference', 'EMAIL')
            reservation.save()
            is_available, result = ReservationService.check_table_availability(
                form.cleaned_data['date'],
                form.cleaned_data['time'],
                form.cleaned_data['number_of_people']
            )
            
            if is_available:
                reservation.table = result
                reservation.save()
                notification_results = ReservationService.send_notifications(reservation)
                
                if notification_results['email'] or notification_results['sms']:
                    messages.success(request, 'Reserva realizada correctamente. Se han enviado las notificaciones.')
                else:
                    messages.warning(request, 'Reserva realizada, pero hubo problemas al enviar las notificaciones.')
                    
                return redirect('reservations:reservas')
            else:
                messages.error(request, result)
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/reservas.html', {'form': form})