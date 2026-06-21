from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.conf import settings

class Organization(models.Model):
    title = models.CharField('Название организации', max_length=100)
    content = models.TextField('Описание')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.title

class Category(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField('Название категории', max_length=200),
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Project(models.Model):
    STATUS_CHOICES = (
        ('current', 'Актуально'),
        ('not_current', 'Не актуально'),
    )

    title = models.CharField('Название проекта', max_length=200)
    location = models.CharField('Место проведения', max_length=200)
    comment = models.TextField('Описание', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, verbose_name='Организация')
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    start_date = models.DateField('Дата начала', null=True, blank=True)
    end_date = models.DateTimeField('Дата окончания')
    number_of_volunteers = models.IntegerField('Количество волонтеров', default=0)
    photo = models.ImageField('Фото проекта', upload_to='project/', blank=True)
    
    latitude = models.FloatField('Широта', null=True, blank=True)
    longitude = models.FloatField('Долгота', null=True, blank=True)
    status = models.CharField('Статус', max_length=50, choices=STATUS_CHOICES, default='current')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

class ResponseProject(models.Model):
    ATTENDANCE_PENDING = 'pending'
    ATTENDANCE_ATTENDED = 'attended'
    ATTENDANCE_MISSED = 'missed'
    ATTENDANCE_CHOICES = (
        (ATTENDANCE_PENDING, 'Ожидает'),
        (ATTENDANCE_ATTENDED, 'Участвовал'),
        (ATTENDANCE_MISSED, 'Не участвовал'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Волонтер')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')
    rating = models.IntegerField('Оценка', default=0)
    attendance_status = models.CharField('Статус участия', max_length=20, choices=ATTENDANCE_CHOICES, default=ATTENDANCE_PENDING)
    created_date = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка на проект'
        verbose_name_plural = 'Заявки на проекты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_response_per_user_project'),
        ]

    def __str__(self):
        return f'{self.user} - {self.project}'
