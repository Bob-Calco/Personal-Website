from django import forms
from django.forms import modelformset_factory
import finances.models as m

class TransactionForm(forms.ModelForm):
    class Meta:
        model = m.Transactions
        fields = ['date', 'amount', 'category', 'specification']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = m.Categories
        fields = ['name', 'description', 'is_income', 'budget', 'specification_of']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['specification_of'].required = False

class BalanceForm(forms.ModelForm):
    class Meta:
        model = m.Balances
        fields = ['date', 'item', 'amount']

BalanceFormSet = modelformset_factory(m.Balances, can_delete=True, fields=('date', 'item', 'amount'), extra=1)

class SearchTermForm(forms.ModelForm):
    class Meta:
        model = m.SearchTerms
        fields = ['dataset', 'term', 'field', 'category', 'specification']

class DatasetForm(forms.ModelForm):
    class Meta:
        model = m.Datasets
        fields = ['name', 'date_field', 'amount_field']

class UploadFileForm(forms.Form):
    file = forms.FileField()
    dataset = forms.ModelChoiceField(queryset=m.Datasets.objects.all())
