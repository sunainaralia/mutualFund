# Generated by Django 4.2.7 on 2023-12-27 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='amount',
            field=models.IntegerField(blank=True, default=0.0),
        ),
        migrations.AddField(
            model_name='transactions',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
