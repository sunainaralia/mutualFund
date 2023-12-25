from django.core.asgi import get_asgi_application
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api.v1.mutual_sip.consumers import SIPConsumer
from api.v1.mutual_sip import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mutualFund.settings")
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
    }
)
