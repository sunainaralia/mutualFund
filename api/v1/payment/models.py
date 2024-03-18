from django.db import models
from api.v1.account.models import User


# Create your models here.
class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction",blank=True)
    invoice = models.CharField(max_length=100)
    date_of_transaction = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    transaction_type = models.CharField(max_length=100, null=True, blank=True)
    amount = models.IntegerField(default=0.0, blank=True)
    transaction_id=models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        # If the object is new and transaction_id is not provided, set it to the id
        if not self.pk and not self.transaction_id:
            last_transaction = Transactions.objects.last()
            if last_transaction:
                self.transaction_id = last_transaction.id + 1
            else:
                self.transaction_id = 1
        super().save(*args, **kwargs)
