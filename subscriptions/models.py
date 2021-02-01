from django.db import models
from profiles.models import UserProfile


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(
        max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class SubscriptionPlan(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    premium = models.BooleanField(default=True)
    image = models.ImageField(
        null=True, blank=True)

    def __str__(self):
        return self.name


class SubscriptionCustomer(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')
    stripeid = models.CharField(max_length=255, default=False)
    stripe_subscription_id = models.CharField(max_length=255, default=False)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)


class SubscriptionRecipe(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField
    premium = models.BooleanField(default=True)
    image = models.ImageField(
        null=True, blank=True)
    added_date = models.DateField(
        auto_now_add=False, auto_now=False, blank=True)

    def __str__(self):
        return self.name