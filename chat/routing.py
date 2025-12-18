# from django.urls import re_path
# from . import 
from django.urls import path
from .consumers import ChatConsumer

wsPattern = [path("ws/messages/<str:room_name>/", ChatConsumer.as_asgi())]