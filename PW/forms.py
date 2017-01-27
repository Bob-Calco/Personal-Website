from django import forms

from .models import memoryScore

class MemoryScoreForm(forms.ModelForm):

    class Meta:
        model = memoryScore
        fields = ('name', 'totalTime', 'time1', 'time2', 'time3', 'time4', 'time5', 'time6', 'time7', 'time8', 'time9', 'turns')
