from django.core.mail import send_mail
from django.conf import settings
import requests

class SMSService:
    @staticmethod
    def format_phone_number(phone):
        # Eliminar cualquier espacio o carácter no numérico
        phone = ''.join(filter(str.isdigit, phone))
        
        # Si no empieza con 56, agregarlo
        if not phone.startswith('56'):
            phone = '56' + phone
            
        # Agregar el + al inicio
        return '+' + phone

    @staticmethod
    def send_sms(phone_number, message):
        # Formatear el número de teléfono
        formatted_phone = SMSService.format_phone_number(phone_number)
        print(f"Número original: {phone_number}")
        print(f"Número formateado: {formatted_phone}")
        
        url = 'https://lq6zyj.api.infobip.com/sms/2/text/advanced'
        
        headers = {
            'Authorization': f'App {settings.INFOBIP_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messages": [
                {
                    "from": "Tregua",
                    "destinations": [{"to": formatted_phone}],
                    "text": message
                }
            ]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"Respuesta de InfoBip: {response.text}")
            
            if response.status_code == 200:
                return True, "SMS enviado correctamente"
            return False, f"Error: {response.text}"
        except Exception as e:
            return False, f"Error: {str(e)}"

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
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reservation.customer_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            return False

    @staticmethod
    def send_sms_notification(reservation):
        message = f'''
        Reserva {reservation.get_status_display()}
        Código: {reservation.confirmation_code}
        Fecha: {reservation.date}
        Hora: {reservation.time}
        '''
        
        success, message = SMSService.send_sms(reservation.customer_phone, message)
        print(f"Resultado SMS: {success} - {message}")
        return success

    @staticmethod
    def send_notifications(reservation):
        results = {
            'email': False,
            'sms': False
        }
        
        if reservation.notification_preference in ['EMAIL', 'BOTH']:
            results['email'] = ReservationService.send_confirmation_email(reservation)

        if reservation.notification_preference in ['SMS', 'BOTH']:
            results['sms'] = ReservationService.send_sms_notification(reservation)

        return results

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

