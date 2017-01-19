from django import forms

from .models import memoryScore

class MemoryScoreForm(forms.ModelForm):

    class Meta:
        model = memoryScore
        fields = ('name', 'time', 'turns')