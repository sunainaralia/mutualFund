# Generated by Django 4.2.7 on 2024-03-29 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mutual_sip', '0014_remove_sip_current_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sip',
            name='sip_photo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
