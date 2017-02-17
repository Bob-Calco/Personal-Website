from django import forms

import scrum.models as m

class UserstoriesForm(forms.ModelForm):

    class Meta:
        model = m.Userstories
        fields = ('name', 'description', 'epic')
