# Generated by Django 3.1.4 on 2021-02-03 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210203_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='stripeid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]