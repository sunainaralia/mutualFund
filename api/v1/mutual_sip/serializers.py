from rest_framework import serializers
from .models import SIP


class SIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIP
        fields = (
            "id",
            "name",
            "current_annual_return_rate",
            "created_at",
            "investment_type",
            "sip_status",
            "users",
            "sip_photo",
            "annual_return_rate",
            "min_amount",
            "description",
            "time_period",
        )

    def create(self, validated_data):
        # Set default value for annual_return_rate if not provided in the request
        annual_return_rate = validated_data.get("annual_return_rate", None)
        if annual_return_rate is None:
            validated_data["annual_return_rate"] = validated_data[
                "current_annual_return_rate"
            ]

        # Create the SIP instance
        instance = super(SIPSerializer, self).create(validated_data)
        return instance

