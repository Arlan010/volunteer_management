from django import template
from organization.models import ResponseProject
from django.db.models import Avg, Count
register = template.Library()

@register.simple_tag()
def response_project(project,user_id):
	response_project = ResponseProject.objects.filter(project = project,user_id = user_id)
	return response_project

@register.simple_tag()
def get_response_project_count(user_id):
	get_response_project_count = ResponseProject.objects.filter(user_id = user_id).count()
	return get_response_project_count
