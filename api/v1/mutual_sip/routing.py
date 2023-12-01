# mutual_fund_project/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from mutualFund.api.v1.mutual_sip.consumers import SIPConsumer

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(
            [
                path("ws/sip/", SIPConsumer.as_asgi()),
            ]
        ),
    }
)
