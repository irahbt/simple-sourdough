from django.contrib import admin

from .models import PlanCustomer



class PlanCustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('stripeid', 'stripe_subscription_id',)

    list_display = ('user_profile',)


admin.site.register(PlanCustomer, PlanCustomerAdmin)
