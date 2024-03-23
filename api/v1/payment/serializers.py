# api/transactions/serializers.py
from rest_framework import serializers
from .models import Transactions
from api.v1.account.models import User,UserPurchaseOrderDetails
from api.v1.mutual_sip.models import SIP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")  # Add any other fields you need


class SIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIP
        fields = ("id", "sip_name")  # Add any other fields you need


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    sip = serializers.PrimaryKeyRelatedField(queryset=SIP.objects.all())
    username = serializers.SerializerMethodField()
    sip_name = serializers.SerializerMethodField()

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
            "transaction_id",
            "status",
            "sip",
            "username",  # Add the username field
            "sip_name",  # Add the sip_name field
        )

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    def get_sip_name(self, obj):
        return obj.sip.name if obj.sip else None

    def validate(self, data):
        user = data.get("user")
        sip = data.get("sip")

        # Check if the user has purchased the SIP
        if not UserPurchaseOrderDetails.objects.filter(user=user, sips=sip).exists():
            raise serializers.ValidationError("The user has not purchased this SIP.")

        return data
