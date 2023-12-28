from django.apps import AppConfig


class YourAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.payment"

    def ready(self):
        import api.v1.payment.signals
