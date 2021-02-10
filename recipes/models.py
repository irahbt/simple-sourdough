from django.db import models


class Ingredient(models.Model):
    class Meta:
           verbose_name_plural = "Ingredients"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    ingredient_list = models.ManyToManyField(Ingredient, related_name='ingredient_list')
    instructions = models.TextField(null=True, blank=True)
    image_url = models.URLField(
        max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    added_date = models.DateField(auto_now_add=False, auto_now=False, blank=True)

    def __str__(self):
        return self.title