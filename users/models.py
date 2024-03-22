import django.contrib.auth.models
from django.db import models


class CustomUser(django.contrib.auth.models.AbstractUser):
    phone = models.CharField(max_length=15)
    hobbies = models.TextField(blank=True).email_valid = models.BooleanField(default=False)
    phone_valid = models.BooleanField(default=False)
    email_valid = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='customuser')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser'
    )

    def __str__(self):
        return self.username
