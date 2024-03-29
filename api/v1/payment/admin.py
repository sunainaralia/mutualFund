from django.contrib import admin
from .models import Transactions


# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "date_of_transaction",
        "invoice",
        "user",
        "transaction_type",
        "amount",
        "transaction_id",
        "status",
        "sip"
    ]


admin.site.register(Transactions, TransactionAdmin)
