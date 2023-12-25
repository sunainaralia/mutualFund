import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SIPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"sip_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def update_current_value(self, event):
        current_value = event["current_value"]
        await self.send(
            text_data=json.dumps(
                {
                    "current_value": current_value,
                }
            )
        )
