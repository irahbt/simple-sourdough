from django import forms
from products.widgets import CustomClearableFileInput
from .models import Ingredient, Recipe


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('recipe',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False


IngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, can_delete=True, extra=1)


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
