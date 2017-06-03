from django import forms
import finances.models as m

class TransactionForm(forms.ModelForm):
    class Meta:
        model = m.Transactions
        fields = ['date', 'amount', 'category', 'specification']
