from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from organization.models import Organization
from volunteers.models import VolunteerProfile

from .models import CustomUser


class OrganizationInline(admin.StackedInline):
    model = Organization
    can_delete = False
    verbose_name_plural = 'Профиль организации (Ұйым профилі)'
    fk_name = 'user'
    extra = 0


class VolunteerProfileInline(admin.StackedInline):
    model = VolunteerProfile
    can_delete = False
    verbose_name_plural = 'Профиль волонтера (Волонтер профилі)'
    fk_name = 'user'
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'rating', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Системные роли и рейтинги', {'fields': ('role', 'rating')}),
    )

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj:
            if obj.role == 1:
                inline_instances.append(VolunteerProfileInline(self.model, self.admin_site))
            elif obj.role == 2:
                inline_instances.append(OrganizationInline(self.model, self.admin_site))
        return inline_instances
