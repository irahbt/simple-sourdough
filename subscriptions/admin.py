from django.contrib import admin

from .models import SubscriptionPlan, SubscriptionRecipe, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(SubscriptionPlan)
admin.site.register(SubscriptionRecipe)
admin.site.register(Category, CategoryAdmin)