from django.db import models

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=30)

class Added(models.Model):
    description = models.CharField(max_length=40)

class Ingredients(models.Model):
    name = models.CharField(max_length=50)

class Recipes(models.Model):
    name = models.CharField(max_length=30)
    howto = models.TextField()
    dateLastUsed = models.DateField()
    ingredients = models.ManyToManyField(Ingredients, through='recipeIngredients')
    tags = models.ManyToManyField(Tags)

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.FloatField()

class GroceryList(models.Model):
    date = models.DateField()
    recipes = models.ManyToManyField(Recipes)
