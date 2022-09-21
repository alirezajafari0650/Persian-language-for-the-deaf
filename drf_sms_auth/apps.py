from django.apps import AppConfig


class DrfSmsAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drf_sms_auth'

    def ready(self):
        from drf_sms_auth.listeners import phone_code_post_save
