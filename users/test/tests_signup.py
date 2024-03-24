from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()

class SignupViewTestCase(APITestCase):
    def test_signup_success(self):
        """Test successful user signup."""
        url = reverse('signup')
        data = {'username': 'newuser', 'first_name': 'name', 'last_name':"ledesma", 'email': 'test@example.com', 'phone': '678285214','hobbies':'Sports'}
        with self.assertNumQueries(4):
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue('Successful register' in response.data['message'])

    def test_signup_failure_user_exists(self):
        """Test signup failure due to existing user."""
        User.objects.create_user(username='existinguser', password='testpassword123', email='existing@example.com')
        url = reverse('signup')
        with self.assertNumQueries(2):
            data = {'username': 'existinguser', 'password': 'newpassword123', 'email': 'testnew@example.com'}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

