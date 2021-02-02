from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_plan, name='checkout_plan'),
]
