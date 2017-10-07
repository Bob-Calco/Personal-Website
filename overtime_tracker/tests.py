from django.test import TestCase
from overtime_tracker.models import Day
from datetime import date

Day.objects.filter(date__gt=date(2017,5,4)).delete()

# Create your tests here.
