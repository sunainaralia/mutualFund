from rest_framework import serializers
from .models import SIP


class SIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIP
        fields = (
            "id",
            "user",
            "name",
            "current_annual_return_rate",
            "min_amount",
            "current_value",
            "time_period",
            "created_at",
            "no_of_investers",
            "total_investment",
            "investment_type",
            "sip_status",
            "gain_value",
        )
