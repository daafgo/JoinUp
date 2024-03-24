
from django.test import TestCase
from users.serializers import UserSerializer

class UserSerializerTest(TestCase):
    def test_create_user_with_valid_data_efficiently(self):
        """Verify that we can create a user with valid data"""
        user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'phone': '+12345678901',
            'hobbies': 'Reading, Swimming'
        }
        with self.assertNumQueries(1):
            serializer = UserSerializer(data=user_data)
            self.assertTrue(serializer.is_valid())
            user = serializer.save()

    def test_create_user_with_invalid_data_efficiently(self):
        """Verify that we can't create a user with errors on the fields """
        invalid_user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'not-an-email',
            'phone': 'invalid_phone',
        }

        with self.assertNumQueries(0):
            serializer = UserSerializer(data=invalid_user_data)
            self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)