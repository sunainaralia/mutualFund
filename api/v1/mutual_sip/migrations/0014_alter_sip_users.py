# Generated by Django 4.2.7 on 2023-12-16 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_delete_usersipdetails'),
        ('mutual_sip', '0013_remove_sip_users_sip_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sip',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='sips_taken', to='account.userpurchaseorderdetails'),
        ),
    ]
