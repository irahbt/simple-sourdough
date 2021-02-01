from django.contrib import admin
from .models import Order, OrderLineItem, SubscriptionOrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class SubscriptionOrderLineItemAdminInline(admin.TabularInline):
    model = SubscriptionOrderLineItem
    readonly_fields = ('subscriptionlineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline, SubscriptionOrderLineItemAdminInline)

    readonly_fields = ('order_number', 'date',
                       'shipping_cost', 'order_total',
                       'grand_total', 'original_basket', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name', 'email', 'phone_number',
              'street_address1', 'street_address2',
              'town_or_city', 'county', 'country', 'postcode',
              'shipping_cost', 'order_total', 'grand_total',
              'original_basket', 'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'shipping_cost', 'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
