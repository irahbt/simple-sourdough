from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions, name='subscriptions'),
    path('config/', views.stripe_config, name='stripe_config'),
]
