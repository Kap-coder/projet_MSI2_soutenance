from django import forms
from .models import Course
from users.models import Department, Filiere, Level

class CourseForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, label="Département")
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), required=False, label="Filière")
    
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'level', 'total_hours', 'teachers']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'teachers': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add data attributes to options for JS filtering
        # Note: This is a bit heavy for large datasets but simple for this scale
        
        # Pre-fetch for performance
        filieres = Filiere.objects.select_related('department').all()
        levels = Level.objects.select_related('filiere').all()
        
        # We can't easily add data attributes to Django ChoiceWidget options standardly without subclassing.
        # So we will pass the mapping to the template via the form instance or context??
        # Hack: attributes on the widget itself don't help for individual options.
        
        # Alternative: We just set the initial values as done before.
        if self.instance.pk and self.instance.level:
            self.initial['filiere'] = self.instance.level.filiere
            self.initial['department'] = self.instance.level.filiere.department
