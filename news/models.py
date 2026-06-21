from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class News(TranslatableModel):
    translations = TranslatedFields(
    	title = models.CharField('Заголовок', max_length = 200),
    	content = models.TextField('Содержание')
    )
    created_date = models.DateTimeField('Дата создания', auto_now_add = True)
    photo = models.ImageField('Фото новости', upload_to='news/', blank=True)

    class Meta:
       verbose_name = 'Новость'
       verbose_name_plural = 'Новости'

    def __str__(self):
       return self.title
