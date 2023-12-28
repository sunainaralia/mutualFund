from django.db import models
from api.v1.account.models import User


# Create your models here.
class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction")
    invoice = models.CharField(max_length=100)
    date_of_transaction = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    transaction_type = models.CharField(max_length=100, null=True, blank=True)
    amount = models.IntegerField(default=0.0, blank=True)



    
