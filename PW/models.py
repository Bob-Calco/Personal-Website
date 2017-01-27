from django.db import models
from django.utils import timezone

# Create your models here.
class memoryScore(models.Model):
    name = models.CharField(max_length=20)
    totalTime = models.FloatField()
    time1 = models.FloatField()
    time2 = models.FloatField()
    time3 = models.FloatField()
    time4 = models.FloatField()
    time5 = models.FloatField()
    time6 = models.FloatField()
    time7 = models.FloatField()
    time8 = models.FloatField()
    time9 = models.FloatField()
    turns = models.IntegerField()
    score = models.FloatField()
    date = models.DateTimeField(default = timezone.now)

    def save(self, *args, **kwargs):
        self.score = round(100-(self.totalTime-10)-(2*(self.turns-10)),1)
        super(memoryScore, self).save(*args, **kwargs)
