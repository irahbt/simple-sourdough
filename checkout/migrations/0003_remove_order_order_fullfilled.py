# Generated by Django 3.1.4 on 2021-03-31 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_order_order_fullfilled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_fullfilled',
        ),
    ]
