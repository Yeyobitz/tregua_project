from django.core.mail import send_mail
from django.conf import settings
from .models import Reservation

class ReservationService:
    @staticmethod
    def send_confirmation_email(reservation):
        subject = f'Confirmación de reserva - {reservation.confirmation_code}'
        message = f'''
        Estimado/a {reservation.customer_name},

        Su reserva ha sido {reservation.get_status_display()}.

        Detalles de la reserva:
        - Código: {reservation.confirmation_code}
        - Fecha: {reservation.date}
        - Hora: {reservation.time}
        - Personas: {reservation.number_of_people}

        Gracias por elegir Tregua Restaurant.
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [reservation.customer_email],
            fail_silently=False,
        )

    @staticmethod
    def check_table_availability(date, time, number_of_people):
        from .models import Table, Reservation
        from django.utils import timezone
        from datetime import datetime, timedelta
    
        # Define time window for reservations
        RESERVATION_DURATION = timedelta(hours=2)
        
        # Convert time to datetime for calculations
        requested_datetime = timezone.make_aware(datetime.combine(date, time))
        end_datetime = requested_datetime + RESERVATION_DURATION
        
        # Get suitable tables
        suitable_tables = Table.objects.filter(
            is_active=True,
            capacity__gte=number_of_people
        ).order_by('capacity')
        
        if not suitable_tables.exists():
            return False, "No hay mesas disponibles para este número de personas."
        
        # Check each table
        for table in suitable_tables:
            conflicting_reservations = Reservation.objects.filter(
                table=table,
                date=date,
                status='CONFIRMED'
            ).exclude(
                time__gte=end_datetime.time(),  # Starts after our end
            ).exclude(
                time__lte=(requested_datetime - RESERVATION_DURATION).time()  # Ends before our start
            )
            
            if not conflicting_reservations.exists():
                return True, table
        
        return False, "No hay mesas disponibles en este horario."

