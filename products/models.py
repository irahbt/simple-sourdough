from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(
        max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(
        max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(
        max_length=1024, null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True)
    added_date = models.DateField(auto_now_add=True, null=True, blank=True)
    featured = models.BooleanField(default=False)
    inventory = models.IntegerField(default=0)
    inventory_updated = models.BooleanField(default=False)

    """
    Inventory code adapted from:
    https://github.com/codingforentrepreneurs/Django-Bootcamp-1/
    """
    def has_inventory(self):
        return self.inventory > 0  # True or False

    def remove_items_from_inventory(self, count, save=True):
        current_inv = self.inventory
        current_inv -= count
        self.inventory = current_inv
        if save is True:
            self.save()
        return self.inventory

    def add_items_back_to_inventory(self, count, save=True):
        current_inv = self.inventory
        current_inv += count
        self.inventory = current_inv
        if save is True:
            self.save()
        return self.inventory

    def __str__(self):
        return self.name
