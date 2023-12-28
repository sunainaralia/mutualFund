# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import Signal
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Transactions

payment_success_signal = Signal()


@receiver(post_save, sender=Transactions)
def handle_payment_success(sender, instance, created, **kwargs):
    if created and instance.transaction_type == "payment" and instance.amount > 0:
        print("Payment success signal triggered")
        payment_success_signal.send(sender=instance.__class__, instance=instance)
