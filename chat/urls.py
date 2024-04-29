from django.urls import path  # Importing the 'path' function from the 'django.urls' module

from . import views  # Importing the 'views' module from the current package

urlpatterns = [
    path('', views.chat, name='messages'),  # Mapping the root URL to the 'chat' view function with the name 'messages'
    path('departments/', views.departments, name='departments'),  # Mapping the '/departments/' URL to the 'departments' view function with the name 'departments'
    path('regions/', views.regions, name='regions'),  # Mapping the '/regions/' URL to the 'regions' view function with the name 'regions'
    path('departments/<slug:slug>/', views.department_message, name='department'),  # Mapping the '/departments/<slug:slug>/' URL to the 'department_message' view function with the name 'department'
    path('regions/<slug:slug>/', views.regions_message, name='region'),  # Mapping the '/regions/<slug:slug>/' URL to the 'regions_message' view function with the name 'region'
]
