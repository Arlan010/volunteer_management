from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Project, Organization, ResponseProject

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    pass

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'category')

@admin.register(ResponseProject)
class ResponseProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_date')