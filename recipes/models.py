from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    image_url = models.URLField(
        max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    premium = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Ingredient(models.Model):
    class Meta:
           verbose_name_plural = "Ingredients"

    name = models.CharField(max_length=100)
    quantity = models.FloatField(null=True, blank=True, default='0')
    unit_of_measurement_choices = [
        ('MILLIGRAMS', 'mg'),
        ('GRAMS', 'g'),
        ('MILLILITERS', 'ml'),
        ('LITERs', 'l'),
        ]
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients")

    def __str__(self):
        return self.name
