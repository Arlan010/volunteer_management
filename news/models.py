from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class News(TranslatableModel):
    translations = TranslatedFields(
    	title = models.CharField(max_length = 200),
    	content = models.TextField()
    )
    created_date = models.DateTimeField(auto_now_add = True)
    photo = models.ImageField(upload_to='news/', blank=True)

    def __str__(self):
       return self.title
