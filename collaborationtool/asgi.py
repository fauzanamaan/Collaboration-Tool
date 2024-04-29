"""
ASGI config for collaborationtool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""


import os

from django.urls import path
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.consumers as consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collaborationtool.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/department/<str:department_name>/',
                 consumers.DepartmentConsumer.as_asgi()),
            path('ws/region/<str:region_name>/',
                 consumers.RegionConsumer.as_asgi()),

        ])
    )
})
