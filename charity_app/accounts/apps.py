from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charity_app.accounts'

    def ready(self):
        import charity_app.accounts.signals
