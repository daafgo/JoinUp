from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from django.core.mail import send_mail
from twilio.rest import Client
from celery import shared_task
import logging

SPAIN_PREFIX = '+(34)'
VERIFICATION_CHANEL = 'sms'
logger = logging.getLogger(__name__)


class SignupAPIView(APIView):

    @staticmethod
    @transaction.atomic
    def post(request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if CustomUser.objects.filter(username=request.data['username']).exists():
                return Response({'error': "This username is in use"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            if settings.ENVIRONMENT == 'prod':
                if not send_confirmation_email.delay(user.email):
                    transaction.set_rollback(True)
                    return Response({'error': "Error sending email, please try again"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                if not send_confirmation_sms.delay(user.phone):
                    transaction.set_rollback(True)
                    return Response({'error': "Error sending SMS, please try again"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(
                {
                    "message": "Successful register, an email and a SMS are being sent to you to confirm your "
                               "registration."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'Please specify the user ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = UserSerializer(user)
            data = serializer.data
            return Response(data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not Found'}, status=status.HTTP_404_NOT_FOUND)


@shared_task
def send_confirmation_email(user_email):
    try:
        subject = 'Register confirmation'
        message = 'Please, confirm your email.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        logger.error('Error on email send: ' + str(e))
        return False


@shared_task
def send_confirmation_sms(user_phone):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        verify = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID)
        verify.verifications.create(to=SPAIN_PREFIX + user_phone, channel=VERIFICATION_CHANEL)
        return True
    except Exception as e:
        logger.error('Error on SMS send: ' + str(e))
        return False
