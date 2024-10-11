from django.apps import AppConfig


class DramaConfig(AppConfig):
    name = 'src.services.drama'
    verbose_name = 'Drama'
    verbose_name_plural = 'Drama'
    default_auto_config = 'django.db.models.BigAutoField'

    def ready(self):
        import src.services.users.signals