from django.contrib import admin

from .models import Subscription, SubscriptionRecipe


admin.site.register(Subscription)
admin.site.register(SubscriptionRecipe)