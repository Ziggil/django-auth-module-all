from django.apps import AppConfig

class AuthModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_module'

    def ready(self):
        import auth_module.signals