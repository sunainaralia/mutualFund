# mutual_fund_app/middleware.py
# from channels.middleware import WebSocketMiddleware
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import AnonymousUser
# from api.v1.account.models import UserPurchaseOrderDetails


# class WebsocketUserMiddleware(WebSocketMiddleware):
#     async def __call__(self, scope, receive, send):
#         scope["user"]._wrapped = await self.get_user(scope)
#         return await super().__call__(scope, receive, send)

#     @database_sync_to_async
#     def get_user(self, scope):
#         if scope["user"].is_anonymous:
#             return AnonymousUser()
#         return UserPurchaseOrderDetails.objects.get(user=scope["user"])
