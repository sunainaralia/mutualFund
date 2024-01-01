# api/transactions/serializers.py
from rest_framework import serializers
from .models import Transactions


class TransactionSerializer(serializers.ModelSerializer):
    # notification_sent = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Transactions
        fields = (
            "id",
            "title",
            "date_of_transaction",
            "invoice",
            "user",
            "transaction_type",
            "amount",
            # "notification_sent",
        )
