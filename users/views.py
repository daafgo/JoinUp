from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import UserSerializer
from django.core.mail import send_mail
from twilio.rest import Client
# Create your views here.
import logging

logger = logging.getLogger(__name__)


class SignupAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if CustomUser.objects.filter(username=request.data['username']).exists():
                return Response({'error': "This username it's in use"}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            try:
                subject = 'Register confirmation'
                message = 'Please, confirm your email.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                logger.error('error on mail send: ' + str(e))
                return Response({'error sending email, please try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                verify = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID)
                verify.verifications.create(to='+(34)' + user.phone, channel='sms')
            except Exception as e:
                logger.error('error on mail send: ' + str(e))
                return Response({'error sending SMS, please try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(
                {"message": "Successful register, an email and a sms are sending to you to confirm your register."},
                status=status.HTTP_201_CREATED)
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
