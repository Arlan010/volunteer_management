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
    role = models.PositiveSmallIntegerField('Роль', choices=USER_ROLE_CHOICES, null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, null=True, blank=True)
    photo = models.ImageField('Фото профиля', upload_to='users/', blank=True)
    rating = models.IntegerField('Рейтинг', default=0)

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_volunteer(self):
        return self.role == USERTYPE_VOLUNTEER

    @property
    def is_organization(self):
        return self.role == USERTYPE_ORGANIZATION

    def __str__(self):
        return self.username


class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Получатель',
    )
    title = models.CharField('Заголовок', max_length=150)
    message = models.TextField('Сообщение')
    url = models.CharField('Ссылка', max_length=255, blank=True)
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.title
