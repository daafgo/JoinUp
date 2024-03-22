from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.core.mail import send_mail
from twilio.rest import Client
# Create your views here.
import logging

logger = logging.getLogger(__name__)
class SignupAPIView(APIView):


    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                subject = 'Confirmación de registro'
                message = 'Por favor, confirma tu correo electrónico.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                logger.error('error on mail send: '+str(e))
                return Response({'error sending email, please try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                verify = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID)
                verify.verifications.create(to='+(34)'+ user.phone, channel='sms')
            except Exception as e:
                logger.error('error on mail send: '+str(e))
                return Response({'error sending SMS, please try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"message": "Successful register, an email and a sms are sending to you to confirm your register."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
