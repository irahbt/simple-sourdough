from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('<int:pk>/', views.recipe, name='recipe'),
]
