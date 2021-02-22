from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions, name='subscriptions'),
    path('subscription_checkout/', views.subscription_checkout, name='subscription_checkout'),
    path('subscription_success/', views.subscription_success, name='subscription_success'),
    path('subscription_cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('subscription_settings/', views.subscription_settings, name='subscription_settings'),
    path('update_accounts/', views.update_accounts, name='update_accounts'),
]
