# Generated by Django 3.1.4 on 2021-04-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_remove_order_order_fullfilled'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_fullfilled',
            field=models.BooleanField(default=True),
        ),
    ]