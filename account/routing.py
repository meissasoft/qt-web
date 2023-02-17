from django.urls import re_path
from . import consumers
from . import scan_consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/socket-server/scan/$', scan_consumers.ScanConsumer.as_asgi()),
]