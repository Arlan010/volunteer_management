from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import News


@admin.register(News)
class NewsAdmin(TranslatableAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('translations__title', 'translations__content')
    readonly_fields = ('created_date',)
