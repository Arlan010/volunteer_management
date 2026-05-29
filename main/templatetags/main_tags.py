from django import template
from organization.models import Project
from account.models import CustomUser
from news.models import News
from main.models import AnswerSupport
from django.db.models import Avg, Count
register = template.Library()

@register.simple_tag()
def news_count():
	news_count = News.objects.all().count()
	return news_count

@register.simple_tag()
def project_count():
	project_count = Project.objects.all().count()
	return project_count
	
@register.simple_tag()
def volunteer_count():
	volunteer_count = CustomUser.objects.filter(role=1).count()
	return volunteer_count

@register.simple_tag()
def answer_support(id):
    try:
        return AnswerSupport.objects.get(support= id)
    except AnswerSupport.DoesNotExist:
        return 'Әлі әкімшіліктен жауап жоқ'
