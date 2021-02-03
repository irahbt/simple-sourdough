from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    premium = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    added_date = models.DateField(auto_now_add=False, auto_now=False, blank=True)

    def __str__(self):
        return self.title