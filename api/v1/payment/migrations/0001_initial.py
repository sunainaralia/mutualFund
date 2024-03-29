# Generated by Django 4.2.7 on 2024-03-17 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.CharField(max_length=100)),
                ('date_of_transaction', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_type', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.IntegerField(blank=True, default=0.0)),
                ('transaction_id', models.IntegerField(blank=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
