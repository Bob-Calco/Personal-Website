from django.db import models
from django.utils import timezone

class Attendee(models.Model):
    STUDENT = 'ST'
    TEACHER = 'TE'
    PARENT = 'PA'
    STAFF = 'SA'
    BOARD_MEMBER = 'BM'
    VOLUNTEER = 'VO'
    ROLE_CHOICES = (
        (STUDENT, 'Leerling'),
        (TEACHER, 'Leraar'),
        (PARENT, 'Actieve ouder'),
        (STAFF, 'Personeel'),
        (BOARD_MEMBER, 'Bestuurslid'),
        (VOLUNTEER, 'Vrijwilliger'),
    )
    START_DATE_CHOICES = [('{}/{}'.format(r, r+1),'{}/{}'.format(r, r+1)) for r in range(1966, 2017)]
    END_DATE_CHOICES = [('{}/{}'.format(r, r+1),'{}/{}'.format(r, r+1)) for r in range(1966, 2017)]
    SKIPPED_CLASS = 1
    REDID_CLASS = -1
    CLASS_CHANGE_CHOICES = ((REDID_CLASS, 'Blijven zitten'), (SKIPPED_CLASS, 'Klas overgeslagen'))
    CLASSES = (
        ('G1', 'Groep 1'),
        ('G2', 'Groep 2'),
        ('G3', 'Groep 3'),
        ('G4', 'Groep 4'),
        ('G5', 'Groep 5'),
        ('G6', 'Groep 6'),
        ('G7', 'Groep 7'),
        ('G8', 'Groep 8'),
        ('K1', 'Klas 1'),
        ('K2', 'Klas 2'),
        ('K3', 'Klas 3'),
        ('K4', 'Klas 4'),
        ('K5', 'Klas 5'),
        ('K6', 'Klas 6'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    maiden_name = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField()
    email = models.EmailField()
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    start_date = models.CharField(max_length=9, choices=START_DATE_CHOICES)
    end_date = models.CharField(max_length=9, choices=END_DATE_CHOICES, null=True, blank=True)
    last_class = models.CharField(max_length=2, choices=CLASSES, null=True, blank=True)
    class_change = models.IntegerField(choices=CLASS_CHANGE_CHOICES, null=True, blank=True)
    class_change_year = models.CharField(max_length=2, choices=CLASSES, null=True, blank=True)
    created_timestamp = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
