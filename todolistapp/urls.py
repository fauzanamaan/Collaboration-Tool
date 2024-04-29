from django.urls import path  # Importing the path function from django.urls module
# Importing the views from the current package
from .views import add_task, display_queue, delete_task

urlpatterns = [
    # Mapping the add_task view to the 'add_task/' URL
    path('add_task/', add_task, name='add_task'),
    # Mapping the display_queue view to the root URL
    path('', display_queue, name='display_queue'),
    # Mapping the delete_task view to the 'delete_task/<int:task_id>/' URL
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
]
