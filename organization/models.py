from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.conf import settings

class Organization(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Category(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200),
    )

    def __str__(self):
        return self.title

class Project(models.Model):
    STATUS_CHOICES = (
        ('current', 'Актуально'),
        ('not_current', 'Не актуально'),
    )

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    comment = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateTimeField()
    number_of_volunteers = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='project/', blank=True)
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='current')

    def __str__(self):
        return self.title

class ResponseProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.user} on project {self.project}'
