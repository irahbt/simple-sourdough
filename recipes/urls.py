from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('<int:recipe_id>/', views.recipe, name='recipe'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
]
