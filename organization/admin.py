from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category,Project,Organization,ResponseProject, VolunteerProject

admin.site.register(Category,TranslatableAdmin)
admin.site.register(Project)
admin.site.register(Organization)
admin.site.register(ResponseProject)
admin.site.register(VolunteerProject)
# Register your models here.
