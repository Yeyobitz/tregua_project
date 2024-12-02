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

    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customer_phone', 'date', 'time', 'number_of_people']

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
    