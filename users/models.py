from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    hobbies = models.TextField(blank=True)
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
