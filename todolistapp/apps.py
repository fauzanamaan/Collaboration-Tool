# Importing the AppConfig class from the django.apps module
from django.apps import AppConfig


class TodolistappConfig(AppConfig):  # Defining a class named TodolistappConfig
    # Setting the default_auto_field attribute to 'django.db.models.BigAutoField'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todolistapp'  # Setting the name attribute to 'todolistapp'
