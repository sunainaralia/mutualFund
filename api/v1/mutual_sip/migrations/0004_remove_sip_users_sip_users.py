# Generated by Django 4.2.7 on 2023-12-02 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_usersipdetails_sips_usersipdetails_sips'),
        ('mutual_sip', '0003_rename_no_of_investers_sip_no_of_investors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sip',
            name='users',
        ),
        migrations.AddField(
            model_name='sip',
            name='users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sip_list', to='account.usersipdetails'),
        ),
    ]
