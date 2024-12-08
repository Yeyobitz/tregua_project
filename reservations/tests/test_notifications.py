from django.test import TestCase
from django.core import mail
from unittest.mock import patch
from datetime import datetime
from ..models import Reservation
from ..services import ReservationService

class NotificationTests(TestCase):
    def setUp(self):
        # Crear una reserva de prueba
        self.reservation = Reservation.objects.create(
            customer_name="Cliente Prueba",
            customer_email="test@example.com",
            customer_phone="+34600000000",
            date=datetime.now().date(),
            time=datetime.now().time(),
            number_of_people=2,
            confirmation_code="TEST123",
            notification_preference='BOTH'
        )

    def test_email_sending(self):
        # Test de envío de email
        ReservationService.send_confirmation_email(self.reservation)
        
        # Verificar que se envió el email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.reservation.customer_email)
        self.assertIn(self.reservation.confirmation_code, mail.outbox[0].subject)

    @patch('twilio.rest.Client')
    def test_sms_sending(self, mock_twilio):
        # Mock de la respuesta de Twilio
        mock_twilio.return_value.messages.create.return_value.sid = 'TEST_SID'
        
        # Test de envío de SMS
        ReservationService.send_sms_notification(self.reservation)
        
        # Verificar que se llamó a Twilio
        mock_twilio.return_value.messages.create.assert_called_once() 