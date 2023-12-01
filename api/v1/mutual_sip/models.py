from django.db import models

# from api.v1.account.models import User
# from api.v1.account.models import UserSipDetails


class SIP(models.Model):
    user = models.ManyToManyField("account.UserSipDetails")
    name = models.CharField(max_length=255)
    current_annual_return_rate = models.FloatField(default=0.0)
    min_amount = models.FloatField(default=0.0)
    current_value = models.FloatField(default=0.0)
    time_period = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_investers = models.IntegerField()
    total_investment = models.FloatField(default=0.0)
    investment_type = models.CharField(max_length=100)
    sip_status = models.CharField(max_length=100, default="active")
    gain_value = models.FloatField(default=0.0)
