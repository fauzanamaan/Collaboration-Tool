# Import the admin module from django.contrib
from django.contrib import admin
# Import the Department and Region models from the current directory
from .models import Department, Region


# Register the Department model with the admin site
admin.site.register(Department)  # Registering Department model

# Register the Region model with the admin site
admin.site.register(Region)  # Registering Region model
