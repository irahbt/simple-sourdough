# Generated by Django 3.1.4 on 2021-02-10 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='premium',
        ),
    ]