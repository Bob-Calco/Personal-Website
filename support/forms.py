from django import forms

import support.models as m

class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = m.SupportMessages
        fields = ['content']
