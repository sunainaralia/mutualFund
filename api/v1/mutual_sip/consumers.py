# mutual_fund_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import SIP


class SIPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        sip_id = self.scope["url_route"]["kwargs"]["sip_id"]
        await self.channel_layer.group_add(f"sip_{sip_id}", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        sip_id = self.scope["url_route"]["kwargs"]["sip_id"]
        await self.channel_layer.group_discard(f"sip_{sip_id}", self.channel_name)

    async def update_current_value(self, event):
        current_value = event["current_value"]
        await self.send(text_data=json.dumps({"current_value": current_value}))
