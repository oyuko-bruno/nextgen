# Generated by Django 5.0.6 on 2024-07-02 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxibooking',
            name='taxi_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
