from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# from api.v1.account.models import UserSipDetails


class SIP(models.Model):
    users = models.ManyToManyField(
        "account.UserPurchaseOrderDetails",
        related_name="sips_taken",
        blank=True,
    )
    name = models.CharField(max_length=255)
    current_annual_return_rate = models.FloatField(default=0.0, blank=True)
    annual_return_rate = models.FloatField(default=0.0)
    min_amount = models.FloatField(default=0.0)
    current_value = models.FloatField(default=0.0, blank=True)
    time_period = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_investors = models.IntegerField(default=0, blank=True, null=True)
    total_investment = models.FloatField(default=0.0, blank=True, null=True)
    investment_type = models.CharField(max_length=100, blank=True, null=True)
    sip_status = models.CharField(max_length=100, default="active")
    gain_value = models.FloatField(default=0.0, blank=True)
    sip_photo = models.ImageField(upload_to="user_image", max_length=300, null=True)

    def calculate_sip_values(self):
        interest = self.current_annual_return_rate
        installment = self.time_period
        installment_amount = self.min_amount
        rate = (interest / 100) / 12
        current_value = (
            installment_amount * (pow(1 + rate, installment) - 1) * (1 + rate) / rate
        )
        total_investment = installment_amount * installment
        total_gain = current_value - total_investment
        gain_percentage = (
            (total_gain / total_investment) * 100 if total_investment != 0 else 0
        )
        return {
            "current_value": current_value,
            "total_gain": total_gain,
            "gain_percentage": gain_percentage,
        }

    def save(self, *args, **kwargs):
        calculated_values = self.calculate_sip_values()
        self.current_value = calculated_values["current_value"]
        self.gain_value = calculated_values["total_gain"]

        super(SIP, self).save(*args, **kwargs)

    def update_current_value(self):
        calculated_values = self.calculate_sip_values()
        self.current_value = calculated_values["current_value"]
        self.gain_value = calculated_values["total_gain"]
        self.save()
