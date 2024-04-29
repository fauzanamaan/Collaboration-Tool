from django.urls import path  # Importing the path function from the django.urls module
from .views import dashboard, frontpage  # Importing the dashboard and frontpage views from the current package

urlpatterns = [
    path('', frontpage, name='frontpage'),  # Mapping the root URL to the frontpage view
    path('dashboard/', dashboard, name='dashboard'),  # Mapping the '/dashboard/' URL to the dashboard view
]
