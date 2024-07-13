# Generated by Django 4.2.13 on 2024-07-12 07:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receptionist_booking_room', '0012_order_orderdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='itemsDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=100)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='OrderDate',
            field=models.DateField(default=datetime.datetime(2024, 7, 12, 8, 54, 13, 133215)),
        ),
    ]