from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.conf import settings

class Organization(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Category(TranslatableModel):
    translations = TranslatedFields(
    	title = models.CharField(max_length = 200),
    )

    def __str__(self):
       return self.title

class Project(models.Model):
    title = models.CharField(max_length = 200)
    location = models.CharField(max_length = 200)
    comment = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)
    organization_id = models.ForeignKey('Organization', on_delete = models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True)
    end_date = models.DateTimeField()
    number_of_volunteers = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='project/', blank=True)
    def __str__(self):
        return self.title

class ResponseProject(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.OneToOneField('Project', on_delete = models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f'User {self.user_id} on project {self.project}'


class VolunteerProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date = models.DateField()
    status = models.CharField(max_length=50, choices=(('current', 'Актуально'), ('not_current', 'Не актуально')))

    def __str__(self):
        return self.title