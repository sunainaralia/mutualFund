# Generated by Django 4.2.7 on 2024-03-19 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mutual_sip', '0013_remove_sip_gain_value_remove_sip_no_of_investors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sip',
            name='current_value',
        ),
    ]
