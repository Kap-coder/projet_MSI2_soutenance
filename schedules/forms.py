from django import forms
from .models import GlobalTimeSlot

class GlobalTimeSlotForm(forms.ModelForm):
    class Meta:
        model = GlobalTimeSlot
        fields = ['day_of_week', 'start_time', 'end_time', 'is_break']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ScheduleGeneratorForm(forms.Form):
    DAYS_CHOICES = [
        (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), 
        (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')
    ]
    
    days = forms.MultipleChoiceField(choices=DAYS_CHOICES, widget=forms.CheckboxSelectMultiple, label="Jours concernés")
    day_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'value': '08:00'}), label="Début de journée")
    day_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'value': '18:00'}), label="Fin de journée")
    slot_duration = forms.IntegerField(min_value=15, initial=120, label="Durée d'un cours (minutes)")
    break_duration = forms.IntegerField(min_value=0, initial=15, label="Pause entre les cours (minutes)")
    include_lunch_break = forms.BooleanField(required=False, initial=True, label="Inclure pause déjeuner")
    lunch_break_start = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'value': '12:00'}), label="Début pause déjeuner")
    lunch_break_duration = forms.IntegerField(required=False, min_value=30, initial=60, label="Durée pause déjeuner (minutes)")
