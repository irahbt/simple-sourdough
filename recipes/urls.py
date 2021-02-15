from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('<int:pk>/', views.recipe, name='recipe'),
    path('add/', views.add_recipe, name='add_recipe'),
]
