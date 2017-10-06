from django import forms
import pj.models as m

class AttendeeForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=('%d-%m-%Y', '%d/%m/%Y', '%d%m%Y'))
    terms = forms.BooleanField(
        error_messages={'required': 'Je moet dit accepteren'},
        label='Ik ga akkoord dat mijn email wordt gebruikt om over deze reunie te communiceren.'
    )
    class Meta:
        model = m.Attendee
        fields = (
            'first_name',
            'last_name',
            'maiden_name',
            'date_of_birth',
            'email',
            'role',
            'start_date',
            'end_date',
            'last_class',
            'class_change',
            'class_change_year',
        )
