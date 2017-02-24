from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=30)
    goal = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Epics(models.Model):
    name = models.CharField(max_length=30)
    goal = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Userstories(models.Model):
    name = models.CharField(max_length=30)
    goal = models.CharField(max_length=100)
    priority = models.IntegerField(default=1000)
    date_added = models.DateTimeField(default = timezone.now)
    epic = models.ForeignKey('Epics', on_delete=models.CASCADE)

    storypoints = models.IntegerField(null=True)
    STATUS_CHOICES = ((0, 'Groom'), (1, 'Ready'), (2, 'Doing'), (3, 'Done'))
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name
