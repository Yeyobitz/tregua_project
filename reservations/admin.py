from django.contrib import admin
from .models import Table, Reservation
from .services import ReservationService

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_active')
    list_filter = ('is_active', 'capacity')
    search_fields = ('number',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code', 'customer_name', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'table')
    search_fields = ('customer_name', 'customer_email', 'confirmation_code')
    readonly_fields = ('confirmation_code', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        # Primero guardamos el modelo
        super().save_model(request, obj, form, change)
        
        # Si es una nueva reserva o el estado cambió a confirmado
        if not change or 'status' in form.changed_data:
            if obj.status == 'CONFIRMED':  # o el estado que uses para confirmar
                notification_results = ReservationService.send_notifications(obj)
                if notification_results['email'] or notification_results['sms']:
                    self.message_user(request, "Notificaciones enviadas correctamente")
                else:
                    self.message_user(request, "Hubo un problema al enviar las notificaciones", level='WARNING')
