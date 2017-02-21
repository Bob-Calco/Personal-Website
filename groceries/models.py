from django.db import models
from django.utils import timezone

# Create your models here.
class Items(models.Model):
    description = models.CharField(max_length=70)
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description

class Recipes(models.Model):
    name = models.CharField(max_length=30)
    howto = models.TextField()
    dateLastUsed = models.DateField(default = timezone.now)

    def __str__(self):
        return self.name
