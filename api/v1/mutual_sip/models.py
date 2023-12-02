from django.db import models
from django.contrib.auth.models import User

# from api.v1.account.models import User
# from api.v1.account.models import UserSipDetails


class SIP(models.Model):
    users = models.ManyToManyField(
        "account.UserSipDetails", related_name="sips_taken", null=True, blank=True
    )
    name = models.CharField(max_length=255)
    current_annual_return_rate = models.FloatField(default=0.0)
    min_amount = models.FloatField(default=0.0)
    current_value = models.FloatField(default=0.0)
    time_period = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_investors = models.IntegerField(default=0, blank=True, null=True)
    total_investment = models.FloatField(default=0.0, blank=True, null=True)
    investment_type = models.CharField(max_length=100)
    sip_status = models.CharField(max_length=100, default="active")
    gain_value = models.FloatField(default=0.0)

    def update_no_of_investors(self):
        self.no_of_investors = self.sip_details.count()
        self.save()


# class SIP(models.Model):
#     name = models.CharField(max_length=255)
#     current_annual_return_rate = models.FloatField(default=0.0)
#     min_amount = models.FloatField(default=0.0)
#     current_value = models.FloatField(default=0.0)
#     time_period = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     no_of_investors = models.IntegerField(default=0, blank=True, null=True)
#     total_investment = models.FloatField(default=0.0, blank=True, null=True)
#     investment_type = models.CharField(max_length=100)
#     sip_status = models.CharField(max_length=100, default="active")
#     gain_value = models.FloatField(default=0.0)

#     def update_no_of_investors(self):
#         self.no_of_investors = self.sip_details.count()
#         self.save()
