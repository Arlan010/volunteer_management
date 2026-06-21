from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'account'
    verbose_name = 'Пользователи'

    def ready(self):
        import account.signals
