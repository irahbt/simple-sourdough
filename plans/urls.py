from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe, name='subscribe'),
    path('<int:pk>/', views.plan, name='plan'),
]
