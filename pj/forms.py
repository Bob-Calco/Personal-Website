from django import forms
import pj.models as m

class AttendeeForm(forms.ModelForm):
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
