# Generated by Django 3.1.4 on 2021-01-27 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20210127_1337'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeSubscription',
            new_name='SubscriptionRecipes',
        ),
    ]