# Generated by Django 5.0.6 on 2024-05-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaxiDriverApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('id_number', models.CharField(max_length=20)),
                ('license_number', models.CharField(max_length=20)),
                ('issuing_authority', models.CharField(max_length=100)),
                ('valid_until', models.DateField()),
                ('license_class', models.CharField(max_length=20)),
                ('vehicle_make_model', models.CharField(max_length=100)),
                ('year_of_manufacture', models.IntegerField()),
                ('registration_number', models.CharField(max_length=20)),
                ('vehicle_photo', models.ImageField(upload_to='vehicle_photos')),
                ('insurance_proof', models.ImageField(upload_to='insurance_proofs')),
                ('background_check', models.BooleanField()),
                ('signature', models.CharField(max_length=100)),
            ],
        ),
    ]
