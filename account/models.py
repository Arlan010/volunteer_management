from django.db import models
from django.contrib.auth.models import AbstractUser

USERTYPE_VOLUNTEER = 1
USERTYPE_ORGANIZATION = 2

class CustomUser(AbstractUser):
    """Расширенная модель пользователя для волонтеров и организаций"""
    USER_ROLE_CHOICES = (
        (USERTYPE_VOLUNTEER, 'Волонтер'),
        (USERTYPE_ORGANIZATION, 'Организация'),
    )
    role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', blank=True)
    rating = models.IntegerField(default=0)

    class Meta:
        db_table = 'custom_user'

    @property
    def is_volunteer(self):
        return self.role == USERTYPE_VOLUNTEER

    @property
    def is_organization(self):
        return self.role == USERTYPE_ORGANIZATION

    def __str__(self):
        return self.username
