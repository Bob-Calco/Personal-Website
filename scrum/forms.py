from django import forms

import scrum.models as m

class EpicForm(forms.ModelForm):
    class Meta:
        model = m.Epics
        fields = ('name', 'goal')

class UserstoriesForm(forms.ModelForm):
    class Meta:
        model = m.Userstories
        fields = ('name', 'goal', 'epic')
