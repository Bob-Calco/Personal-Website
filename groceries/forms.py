from django import forms

import groceries.models as m

class RecipeForm(forms.ModelForm):
    class Meta:
        model = m.Recipes
        fields =  ['name' , 'howto']

class ItemForm(forms.ModelForm):
    class Meta:
        model = m.Items
        fields = ['description']

ItemFormSet = forms.inlineformset_factory(m.Recipes, m.Items, can_delete=True, form=ItemForm, fields=('description',))
