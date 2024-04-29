"""
URL configuration for collaborationtool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Import the admin module
from django.conf import settings  # Import the settings module
# Import the path and include functions from the urls module
from django.urls import path, include
# Import the static function from the urls module
from django.conf.urls.static import static


urlpatterns = [
    # Map the 'admin/' URL to the admin.site.urls view
    path('admin/', admin.site.urls),
    # Map the root URL to the dashboard.urls view
    path('', include('dashboard.urls')),
    # Map the 'accounts/' URL to the django.contrib.auth.urls view
    path('accounts/', include('django.contrib.auth.urls')),
    # Map the 'accounts/' URL to the accounts.urls view
    path('accounts/', include('accounts.urls')),
    # Map the 'calendar/' URL to the cal.urls view
    path('calendar/', include('cal.urls')),
    # Map the 'chat/' URL to the chat.urls view
    path('chat/', include('chat.urls')),
    # Map the 'tasks/' URL to the todolistapp.urls view
    path('tasks/', include('todolistapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  # Add the media URL pattern to urlpatterns
                          # Set the document root for the media URL pattern
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,  # Add the static URL pattern to urlpatterns
                          # Set the document root for the static URL pattern
                          document_root=settings.STATIC_ROOT)
