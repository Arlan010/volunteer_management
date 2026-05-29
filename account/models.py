from django.db import models
from django.contrib.auth.models import AbstractUser

USERTYPE_VOLUNTEER = 1
USERTYPE_EXPERT = 2

class CustomUser(AbstractUser):
    """Расширенная пользовательская модель"""
    USER_ROLE_CHOICES = (
        (USERTYPE_VOLUNTEER, 'volunteer'),
        (USERTYPE_EXPERT, 'expert'),
    )
    role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', blank=True)
    rating = models.CharField(max_length=5, default=90)
    class Meta(object):
        db_table = 'custom_user'

    def __str__(self):
        return self.username
