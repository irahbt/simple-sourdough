from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class SubscriptionRecipe(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField
    premium = models.BooleanField(default=True)

    def __str__(self):
        return self.name