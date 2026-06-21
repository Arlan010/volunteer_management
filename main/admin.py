from django.contrib import admin

from .models import AnswerSupport, HomeStatistic, Support


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_id', 'created_date')
    search_fields = ('title', 'user_id__username', 'user_id__email')
    readonly_fields = ('created_date',)


@admin.register(AnswerSupport)
class AnswerSupportAdmin(admin.ModelAdmin):
    list_display = ('support', 'created_date')
    search_fields = ('content', 'support__title')
    readonly_fields = ('created_date',)


@admin.register(HomeStatistic)
class HomeStatisticAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Активные волонтеры', {
            'fields': ('active_volunteers_value', 'active_volunteers_label'),
        }),
        ('Завершенные проекты', {
            'fields': ('completed_projects_value', 'completed_projects_label'),
        }),
    )

    def has_add_permission(self, request):
        if HomeStatistic.objects.exists():
            return False
        return super().has_add_permission(request)
# Register your models here.
