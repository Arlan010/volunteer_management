from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from organization.models import Organization
from volunteers.models import VolunteerProfile

from .models import CustomUser, Notification


class OrganizationInline(admin.StackedInline):
    model = Organization
    can_delete = False
    verbose_name = 'Профиль организации'
    verbose_name_plural = 'Профиль организации'
    fk_name = 'user'
    extra = 0


class VolunteerProfileInline(admin.StackedInline):
    model = VolunteerProfile
    can_delete = False
    verbose_name = 'Профиль волонтера'
    verbose_name_plural = 'Профиль волонтера'
    fk_name = 'user'
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'email', 'phone', 'role', 'rating', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'email', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('Платформа волонтерства', {'fields': ('role', 'phone', 'photo', 'rating')}),
    )

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj:
            if obj.role == 1:
                inline_instances.append(VolunteerProfileInline(self.model, self.admin_site))
            elif obj.role == 2:
                inline_instances.append(OrganizationInline(self.model, self.admin_site))
        return inline_instances


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username', 'recipient__email')
    readonly_fields = ('created_at',)
