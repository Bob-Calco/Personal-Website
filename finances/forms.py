from django import forms
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
