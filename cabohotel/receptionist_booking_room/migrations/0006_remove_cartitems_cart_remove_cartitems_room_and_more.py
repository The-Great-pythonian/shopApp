# Generated by Django 4.2.13 on 2024-06-27 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receptionist_booking_room', '0005_alter_roomsdetails_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitems',
            name='room',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItems',
        ),
    ]
