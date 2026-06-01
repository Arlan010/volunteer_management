from django import template
from organization.models import Project
from news.models import News
from django.db.models import Avg, Count
register = template.Library()

@register.simple_tag()
def news_count():
	news_count = News.objects.all().count()
	return news_count
