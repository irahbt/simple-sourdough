from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions, name='subscriptions'),
    path('stripe_config/', views.stripe_config, name='stripe_config'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('subscription_success/', views.subscription_success, name='subscription_success'),
    path('subscription_cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
