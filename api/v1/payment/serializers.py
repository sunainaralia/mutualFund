from rest_framework import serializers
from .models import Transactions


class TransactionSerializer(serializers.ModelSerializer):
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
        )
