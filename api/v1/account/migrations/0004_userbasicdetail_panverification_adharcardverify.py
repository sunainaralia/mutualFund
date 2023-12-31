# Generated by Django 4.2.7 on 2023-11-08 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_profile_photo_alter_user_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBasicDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nationality', models.CharField(max_length=40)),
                ('fullName', models.CharField(max_length=50)),
                ('d_o_b', models.DateField()),
                ('address_details', models.TextField()),
                ('zip_code', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PanVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pan_card', models.ImageField(max_length=300, upload_to='user_image')),
                ('pan_no', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdharCardVerify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adhar_card_front', models.ImageField(max_length=300, upload_to='user_image')),
                ('adhar_card_back', models.ImageField(max_length=300, upload_to='user_image')),
                ('adhar_no', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
