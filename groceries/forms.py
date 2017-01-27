from django import forms

from .models import Added

class AddedForm(forms.ModelForm):

    class Meta:
        model = Added
        fields = ('description',)
