# Generated by Django 4.2.7 on 2024-03-19 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mutual_sip', '0011_remove_sip_detailss_sip_delete_sip_details_and_more'),
        ('account', '0003_alter_userpurchaseorderdetails_sips'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpurchaseorderdetails',
            name='sips',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_purchase_order_details', to='mutual_sip.sip'),
        ),
        migrations.AlterField(
            model_name='userpurchaseorderdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_userpurchasedetails', to=settings.AUTH_USER_MODEL),
        ),
    ]
