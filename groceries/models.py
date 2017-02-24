from django.db import models
from django.utils import timezone

class Items(models.Model):
    description = models.CharField(max_length=70)
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default = 0)

    def __str__(self):
        return self.description

class Recipes(models.Model):
    name = models.CharField(max_length=30)
    howto = models.TextField()
    dateLastUsed = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name

class GroceryLists(models.Model):
    date = models.DateTimeField(default = timezone.now)
    items = models.ManyToManyField(Items)
    recipes = models.ManyToManyField(Recipes)
    finished = models.BooleanField(default = 0)
