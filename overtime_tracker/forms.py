from django import forms

import overtime_tracker.models as m

class DayForm(forms.ModelForm):
    class Meta:
        model = m.Day
        fields = ['date', 'hours_worked', 'hours_vacation', 'holiday', 'hours_standby']

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = m.Configuration
        fields = '__all__'

class VacationHoursForm(forms.ModelForm):
    class Meta:
        model = m.VacationHours
        fields = '__all__'
