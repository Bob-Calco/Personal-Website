from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

class Items(models.Model):
    user = models.ForeignKey(User, null=True)
    description = models.CharField(max_length=70)
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default = 0)

    def __str__(self):
        return self.description

class Recipes(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=30)
    howto = models.TextField()
    dateLastUsed = models.DateTimeField(default = datetime(2016,1,1,3,14,12))

    def __str__(self):
        return self.name

class GroceryLists(models.Model):
    user = models.ForeignKey(User, null=True)
    date = models.DateTimeField(default = timezone.now)
    items = models.ManyToManyField(Items)
    recipes = models.ManyToManyField(Recipes)
    finished = models.BooleanField(default = 0)
