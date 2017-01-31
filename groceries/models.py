from django.db import models

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Added(models.Model):
    description = models.CharField(max_length=40)

    def __str__(self):
        return self.description

class Ingredients(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Recipes(models.Model):
    name = models.CharField(max_length=30)
    howto = models.TextField()
    dateLastUsed = models.DateField()
    ingredients = models.ManyToManyField(Ingredients, through='recipeIngredients')
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.FloatField()

class GroceryList(models.Model):
    date = models.DateField()
    recipes = models.ManyToManyField(Recipes)

    def __str__(self):
        return self.date
