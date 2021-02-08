from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions, name='subscriptions'),
    path('stripe_config/', views.stripe_config, name='stripe_config'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
]
