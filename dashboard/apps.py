from django.apps import AppConfig

class DashboardConfig(AppConfig):
    # Set the default auto field for models to BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Set the name of the app to 'dashboard'
    name = 'dashboard'
