from django.db import models


class RecipePlan(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    premium = models.BooleanField(default=True)


    def __str__(self):
        return self.title