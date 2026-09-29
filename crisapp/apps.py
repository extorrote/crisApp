from django.apps import AppConfig


class CrisappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crisapp'

    def ready(self):
        import crisapp.signals