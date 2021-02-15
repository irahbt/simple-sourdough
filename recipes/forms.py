from django import forms
from .models import Ingredient, Recipe


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ingredients = Ingredient.objects.all()
        names = [(i.id, i.__str__()) for i in ingredients]

        self.fields['ingredient_list'].choices = names