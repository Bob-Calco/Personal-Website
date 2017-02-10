from django import forms

from .models import memoryScore

class MemoryScoreForm(forms.ModelForm):

    class Meta:
        model = memoryScore
        fields = ('name', 'totalTime', 'time1', 'time2', 'time3', 'time4', 'time5', 'time6', 'time7', 'time8', 'time9', 'turns')

class EncryptForm(forms.Form):
    crypt = forms.ChoiceField(choices = (("encrypt", "Encrypt"), ("decrypt", "Decrypt")), widget=forms.Select(attrs={"onChange": "cryptChange()"}))
    text = forms.CharField(label="Text", widget=forms.Textarea)
    method = forms.ChoiceField(choices = (("caesar", "Caesarian cipher"), ("affine", "Affine cipher"), ("atbash", "Atbash cipher")), widget=forms.Select(attrs={"onChange": "cipherChange()"}) )

    int_key1 = forms.IntegerField(required=False)
    int_key2 = forms.IntegerField(required=False)

    def keys(self):
        if self.cleaned_data['method'] == "caesar":
            return self.cleaned_data['int_key1']
        elif self.cleaned_data['method'] == "affine":
            return (self.cleaned_data['int_key1'], self.cleaned_data['int_key2'])
        else:
            return None
