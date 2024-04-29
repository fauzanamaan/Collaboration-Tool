from django.contrib import admin
from cal.models import Event

# Event model registered with the admin site
admin.site.register(Event)
