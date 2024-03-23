from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from users.models import CustomUser

User = get_user_model()

class SignupAPITestCase(APITestCase):

    def test_signup_success(self):
        """Test successful user signup."""
        url = reverse('signup')
        data = {'username': 'newuser', 'first_name': 'name', 'last_name':"ledesma", 'email': 'test@example.com', 'phone': '678285214','hobbies':'Sports'}
        response = self.client.post(url, data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('Successful register' in response.data['message'])

    def test_signup_failure_user_exists(self):
        """Test signup failure due to existing user."""
        User.objects.create_user(username='existinguser', password='testpassword123', email='existing@example.com')
        url = reverse('signup')
        data = {'username': 'existinguser', 'password': 'newpassword123', 'email': 'testnew@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileViewTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username= 'newuser', first_name= 'name', last_name="ledesma", email= 'test@example.com', phone= '678285214',hobbies='Sports')
        self.url = reverse('user_profile')

    def test_user_profile_success(self):
        """Test successful retrieval of user profile."""
        data = {'user_id': self.user.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_profile_failure_user_not_found(self):
        """Test failure due to user not found."""
        data = {'user_id': 999}  # Asumiendo que este ID no existe
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
