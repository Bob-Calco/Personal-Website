from django.db import models
from django.urls import reverse
from datetime import date

class Day(models.Model):
    date = models.DateField(unique=True)
    hours_worked = models.FloatField(default=0)
    hours_overtime = models.FloatField()
    hours_vacation = models.FloatField(default=0)
    holiday = models.BooleanField(default=False)
    hours_standby = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        c_date = Configuration.objects.filter(date__lte=self.date).aggregate(models.Max('date'))['date__max']
        config = Configuration.objects.filter(date=c_date)[0]
        self.hours_overtime = self.calculate_overtime(config.break_time, config.working_time_until_break)

        self.hours_worked = round(self.hours_worked, 2)
        self.hours_overtime = round(self.hours_overtime, 2)
        self.hours_vacation = round(self.hours_vacation, 2)
        self.hours_standby = round(self.hours_standby, 2)
        super(Day, self).save(*args, **kwargs)

    def calculate_overtime(self, break_time, working_time_until_break):
        if self.holiday or self.date.weekday() in [5, 6]:
            return self.hours_worked
        t = self.hours_worked - (8 - self.hours_vacation)
        if self.hours_worked >= working_time_until_break:
            t -= break_time
        t += self.hours_standby / 20
        return t

    def get_absolute_url(self):
        return reverse('overtime_tracker:update_day', kwargs={'pk': str(self.id)})

    def __str__(self):
        return str(self.date)

class Configuration(models.Model):
    date = models.DateField()
    break_time = models.FloatField()
    working_time_until_break = models.FloatField()

    def get_absolute_url(self):
        return reverse('overtime_tracker:update_config', kwargs={'pk': str(self.id)})

    def __str__(self):
        return str(self.date)

class VacationHours(models.Model):
    year = models.DateField()
    amount = models.FloatField()

    def save(self, *args, **kwargs):
        self.year = date(self.year.year, 1 ,1)
        super(VacationHours, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('overtime_tracker:update_vacation_hours', kwargs={'pk': str(self.id)})

    def __str__(self):
        return str(self.year)
