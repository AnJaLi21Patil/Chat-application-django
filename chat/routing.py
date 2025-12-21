# # from django.urls import re_path
# # from . import 
# from django.urls import path
# from .consumers import ChatConsumer

# wsPattern = [path("ws/messages/<str:room_name>/", ChatConsumer.as_asgi())]
from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[\w_]+)/$', ChatConsumer.as_asgi()),
]
