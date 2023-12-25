from django.urls import re_path
from .consumers import SIPConsumer

websocket_urlpatterns = [
    re_path(r"ws/sip/(?P<user_id>\w+)/$", SIPConsumer.as_asgi()),
]
