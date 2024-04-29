from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/region/<str:region_name>/',  # URL pattern for region websocket connection
         # RegionConsumer class used for handling region websocket connections
         consumers.RegionConsumer.as_asgi()),
    path('ws/department/<str:department_name>/',  # URL pattern for department websocket connection
         # DepartmentConsumer class used for handling department websocket connections
         consumers.DepartmentConsumer.as_asgi()),
]
