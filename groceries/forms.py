from django import forms

import groceries.models as m

class AddedForm(forms.ModelForm):

    class Meta:
        model = m.Added
        fields = ('description',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = m.Recipes
        fields =  ['name' , 'howto']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = m.Ingredients
        fields = ['name', 'unit']
IngredientFormSet = forms.formset_factory(IngredientForm)

class RecipeIngredientsForm(forms.ModelForm):
    class meta:
        model = m.RecipeIngredients
        fields = ['amount']

class TagForm(forms.ModelForm):
    class Meta:
        model = m.Tags
        fields = ['name']
TagFormSet = forms.formset_factory(TagForm)
