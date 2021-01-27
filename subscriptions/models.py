from django.db import models
from django.contrib.auth.models import User


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField
    user_subscribed = models.BooleanField(default=True)
