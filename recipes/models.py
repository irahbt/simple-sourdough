from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    ingredients = models.TextField(null=True, blank=True)
    recipe_text = models.TextField(null=True, blank=True)
    image_url = models.URLField(
        max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    added_date = models.DateField(auto_now_add=False, auto_now=False, blank=True)

    def __str__(self):
        return self.title