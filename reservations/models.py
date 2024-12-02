from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.number} (Capacidad: {self.capacity})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('CONFIRMED', 'Confirmada'),
        ('REJECTED', 'Rechazada'),
        ('CANCELLED', 'Cancelada'),
    ]

    NOTIFICATION_CHOICES = [
        ('EMAIL', 'Correo electrónico'),
        ('SMS', 'SMS'),
        ('BOTH', 'Ambos'),
    ]

    REMINDER_CHOICES = [
        (24, '24 horas antes'),
        (48, '48 horas antes'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notification_preference = models.CharField(max_length=5, choices=NOTIFICATION_CHOICES, default='EMAIL')
    reminder_preference = models.IntegerField(choices=REMINDER_CHOICES, default=24)
    confirmation_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.date:  # Add this check
            if self.date < timezone.now().date():
                raise ValidationError('No se pueden hacer reservaciones en fechas pasadas')

        
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()
        super().save(*args, **kwargs)

    def generate_confirmation_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def __str__(self):
        return f"Reserva {self.confirmation_code} - {self.customer_name}"
