from channels.consumer import SyncConsumer, AsyncConsumer

import json
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("connection is occured", event)
        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        print(event, "msg is recived from client", event["text"])

    def websocket_disconnect(self, event):
        print("websocket is disconnected")


class NotificationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("websocket is connected.....")
        await self.send({"type": "websocket.accept"})

    async def websocket_disconnect(self, close_code):
        pass

    async def websocket_receive(self, event):
        message = event["message"]

        print("Sending notification:", message)
        await self.send(text_data=json.dumps({"message": message}))



