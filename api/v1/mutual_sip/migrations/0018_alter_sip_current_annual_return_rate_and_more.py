# Generated by Django 4.2.7 on 2023-12-26 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mutual_sip', '0017_alter_sip_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sip',
            name='current_annual_return_rate',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='sip',
            name='current_value',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='sip',
            name='gain_value',
            field=models.FloatField(blank=True, default=0.0),
        ),
    ]
