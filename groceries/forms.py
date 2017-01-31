from django import forms

import groceries.models as m

class AddedForm(forms.ModelForm):

    class Meta:
        model = m.Added
        fields = ('description',)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = m.Recipes
        fields =  ['name' , 'howto', 'ingredients', 'tags']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields["ingredients"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["ingredients"].help_text = ""
        self.fields["ingredients"].queryset = m.Ingredients.objects.all()
        self.fields["tags"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["tags"].help_text = ""
        self.fields["tags"].queryset = m.Tags.objects.all()
