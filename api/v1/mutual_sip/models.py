from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class SIP(models.Model):
    users = models.ManyToManyField(
        "account.UserPurchaseOrderDetails",
        related_name="sips_taken",
        blank=True,
    )
    name = models.CharField(max_length=255)
    current_annual_return_rate = models.FloatField(default=0.0, blank=True)
    annual_return_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    investment_type = models.CharField(max_length=100, blank=True, null=True)
    sip_status = models.CharField(max_length=100, default="active")
    sip_photo = models.ImageField(upload_to="user_image", max_length=300, null=True)
    min_amount = models.IntegerField(blank=True, default=0.0, null=True)
    description = models.CharField(max_length=1000, null=True)
    time_period = models.IntegerField(null=True,blank=True)



