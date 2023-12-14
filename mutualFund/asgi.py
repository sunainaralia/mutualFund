# mutual_fund_project/asgi.py
import os
from django.core.asgi import get_asgi_application
from mutualFund.api.v1.mutual_sip.routing import application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mutual_fund_project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": application,
    }
)
