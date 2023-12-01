# mutual_fund_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import SIP


class SIPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        rate = data.get("rate", None)

        if rate is not None:
            # Update the SIP model with the new rate
            sip_instance = SIP.objects.first()
            sip_instance.current_annual_return_rate = rate
            sip_instance.save()

            # Broadcast the updated rate to all connected clients
            await self.send(text_data=json.dumps({"rate": rate}))
