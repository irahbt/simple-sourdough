# Generated by Django 3.1.4 on 2021-02-15 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210215_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='added_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
