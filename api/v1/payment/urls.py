from django.urls import path
from .views import TransactionView, GetTransactionView, GetTransactionThroughUserId

urlpatterns = [
    path("transaction/", TransactionView.as_view()),
    path("getTransaction/<pk>/", GetTransactionView.as_view()),
    path("GetTransactionThroughUserId/<pk>/", GetTransactionThroughUserId.as_view()),
]
