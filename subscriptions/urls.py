from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions, name='subscriptions'),
    path('checkout_subscription/', views.checkout_subscription, name='checkout_subscription'),
]
