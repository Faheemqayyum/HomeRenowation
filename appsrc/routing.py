from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/messages/(?P<room_name>[\w\s]+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"wss/messages/(?P<room_name>[\w\s]+)/$", consumers.ChatConsumer.as_asgi()),
]