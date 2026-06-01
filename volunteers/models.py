from django.conf import settings
from django.db import models


class VolunteerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='volunteer_profile',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Профиль волонтера: {self.user.username}"
