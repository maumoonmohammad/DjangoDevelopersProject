from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"


    def ready(self):  ## this functions lets know there are signals in a different file for this app
        import users.signals
