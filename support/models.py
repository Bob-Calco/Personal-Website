from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SupportMessages(models.Model):
    user = models.ForeignKey(User)
    reply = models.BooleanField(default = 0)
    read = models.BooleanField(default = 0)
    delivered = models.BooleanField(default = 0)
    date = models.DateTimeField(default = timezone.now)
    content = models.TextField()

    def __str__(self):
        return self.content
