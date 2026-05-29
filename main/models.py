from django.db import models
from django.conf import settings

# Create your models here.
class Support(models.Model):
    title = models.CharField(max_length = 100)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

class AnswerSupport(models.Model):
    content = models.TextField()
    support = models.ForeignKey('Support', on_delete = models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.content
   