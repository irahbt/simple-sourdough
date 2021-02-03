from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_subscription, name='checkout_subscription'),
]
