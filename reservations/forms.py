from django import forms
from .models import Reservation
from django.utils import timezone
from django.core.exceptions import ValidationError

class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Fecha'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label='Hora'
    )
    customer_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombre Completo'
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Correo Electrónico'
    )
    customer_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Teléfono'
    )
    number_of_people = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '8'}),
        label='Número de Personas'
    )
    notification_preference = forms.ChoiceField(
        choices=Reservation.NOTIFICATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Preferencia de Notificación'
    )

    class Meta:
        model = Reservation
        fields = [
            'customer_name', 
            'customer_email', 
            'customer_phone', 
            'date', 
            'time', 
            'number_of_people',
            'notification_preference'
        ]

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
    
        if date and time:
            # Create timezone-aware datetime
            reservation_datetime = timezone.make_aware(
                timezone.datetime.combine(date, time)
            )
            if reservation_datetime < timezone.now():
                raise ValidationError('La fecha y hora de reserva debe ser futura')
    
        return cleaned_data
    
    def clean_number_of_people(self):
        number_of_people = self.cleaned_data.get('number_of_people')
        if number_of_people < 1 or number_of_people > 8:
            raise forms.ValidationError('El número de personas debe estar entre 1 y 8.')
        return number_of_people
    