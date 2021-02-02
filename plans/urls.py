from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe, name='subscribe'),
    path('checkout_for_plan/', views.checkout_for_plan, name='checkout_for_plan'),
]
