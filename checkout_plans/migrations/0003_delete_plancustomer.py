# Generated by Django 3.1.4 on 2021-02-03 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout_plans', '0002_remove_plancustomer_membership'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PlanCustomer',
        ),
    ]