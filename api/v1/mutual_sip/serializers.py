from rest_framework import serializers
from .models import SIP


class SIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIP
        fields = (
            "id",
            "name",
            "current_annual_return_rate",
            "min_amount",
            "current_value",
            "time_period",
            "created_at",
            "total_investment",
            "investment_type",
            "sip_status",
            "gain_value",
            "no_of_investors",
            "users",
            "sip_photo",
            "annual_return_rate",
        )
