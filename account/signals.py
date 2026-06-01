from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from organization.models import Organization
from volunteers.models import VolunteerProfile


User = get_user_model()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if instance.is_volunteer:
        VolunteerProfile.objects.get_or_create(user=instance)
    elif instance.is_organization:
        Organization.objects.get_or_create(
            user=instance,
            defaults={
                'title': f"Организация {instance.username}",
                'content': '',
            },
        )
