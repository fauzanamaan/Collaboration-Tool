# Importing the AppConfig class from the django.apps module
from django.apps import AppConfig


# Defining a class named MessagesConfig that inherits from AppConfig
class MessagesConfig(AppConfig):
    # Setting the default_auto_field attribute to 'django.db.models.BigAutoField'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'  # Setting the name attribute to 'chat'
