from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Project, Organization, ResponseProject

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    search_fields = ('title', 'user__username', 'user__email')

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('title',)
    search_fields = ('translations__title',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'location', 'status', 'number_of_volunteers', 'start_date', 'end_date')
    list_filter = ('status', 'category', 'organization')
    search_fields = ('title', 'location', 'organization__title')
    readonly_fields = ('created_date',)

@admin.register(ResponseProject)
class ResponseProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'attendance_status', 'rating', 'created_date')
    list_filter = ('attendance_status', 'project')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'project__title')
    readonly_fields = ('created_date',)
