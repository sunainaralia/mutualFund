# routing.py
from django.urls import path
from .consumers import MySyncConsumer, NotificationConsumer

websocket_urlpatterns = [path("ws/ac/", NotificationConsumer.as_asgi())]
