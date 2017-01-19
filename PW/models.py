from django.db import models
from django.utils import timezone

# Create your models here.
class memoryScore(models.Model):
    name = models.CharField(max_length=20)
    time = models.FloatField()
    turns = models.IntegerField()
    score = models.FloatField()
    date = models.DateTimeField(default = timezone.now)

    def save(self, *args, **kwargs):
        self.score = round(100-(self.time-10)-(2*(self.turns-10)),1)
        super(memoryScore, self).save(*args, **kwargs)