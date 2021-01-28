# Generated by Django 3.1.4 on 2021-01-28 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_auto_20210128_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='category',
        ),
        migrations.AddField(
            model_name='subscription',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.category'),
        ),
    ]