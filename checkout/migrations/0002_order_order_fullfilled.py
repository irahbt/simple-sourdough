# Generated by Django 3.1.4 on 2021-03-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_fullfilled',
            field=models.BooleanField(default=True),
        ),
    ]
