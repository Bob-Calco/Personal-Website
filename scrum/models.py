from django.db import models
from django.utils import timezone

# Create your models here.
class Epics(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

class Userstories(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    priority = models.IntegerField()
    date_added = models.DateTimeField(default = timezone.now)
    epic = models.ForeignKey('Epics', on_delete=models.CASCADE)

    STATUS_CHOICES = ((0, 'Groom'), (1, 'Ready'), (2, 'Doing'), (3, 'Done'))
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
