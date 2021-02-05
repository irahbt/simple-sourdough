from django.urls import path
from . import views
from checkout.webhooks import webhook

urlpatterns = [
    path('', views.checkout_subscription, name='checkout_subscription'),
    path('wh/', webhook, name='webhook'),
]