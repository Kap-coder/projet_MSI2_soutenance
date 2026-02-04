from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'department', 'level', 'teachers']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'teachers': forms.CheckboxSelectMultiple(),
        }
