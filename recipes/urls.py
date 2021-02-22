from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('<int:recipe_id>/', views.recipe, name='recipe'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('edit_ingredient/<int:ingredient_id>/', views.edit_ingredient, name='edit_ingredient'),
    path('delete_ingredient/<int:ingredient_id>/', views.delete_ingredient, name='delete_ingredient'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
