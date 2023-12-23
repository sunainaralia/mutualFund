# mutual_fund_app/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import SIPConsumer

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(
            [
                path("ws/sip/<int:sip_id>/", SIPConsumer.as_asgi()),
            ]
        ),
    }
)
