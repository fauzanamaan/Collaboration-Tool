from django.apps import AppConfig


class AccountsConfig(AppConfig):
    # Set the default auto field for the model
    # Use a big auto field for the model
    default_auto_field = 'django.db.models.BigAutoField'

    # Set the name of the app
    name = 'accounts'  # Name of the app is 'accounts'
