from django.apps import AppConfig


class DictionaryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dictionary"

    def ready(self):
        from . import signals  # noqa: I001,E261,F401
