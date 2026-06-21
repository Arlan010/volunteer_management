from django.db import models
from django.conf import settings

# Create your models here.
class Support(models.Model):
    title = models.CharField('Тема обращения', max_length = 100)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_date = models.DateTimeField('Дата создания', auto_now_add = True)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return self.title

class AnswerSupport(models.Model):
    content = models.TextField('Ответ')
    support = models.ForeignKey('Support', on_delete = models.CASCADE, verbose_name='Обращение')
    created_date = models.DateTimeField('Дата создания', auto_now_add = True)

    class Meta:
        verbose_name = 'Ответ на обращение'
        verbose_name_plural = 'Ответы на обращения'

    def __str__(self):
        return self.content


class HomeStatistic(models.Model):
    active_volunteers_value = models.CharField('Число активных волонтеров', max_length=30, default='1,500+')
    active_volunteers_label = models.CharField('Подпись активных волонтеров', max_length=100, default='Белсенді волонтерлер')
    completed_projects_value = models.CharField('Число завершенных проектов', max_length=30, default='350+')
    completed_projects_label = models.CharField('Подпись завершенных проектов', max_length=100, default='Аяқталған жобалар')

    class Meta:
        verbose_name = 'Статистика главной страницы'
        verbose_name_plural = 'Статистика главной страницы'

    def __str__(self):
        return 'Главная статистика'
   
