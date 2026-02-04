from django import forms
from .models import Course
from users.models import Department, Filiere, Level

class CourseForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, label="Département")
    # Filiere is now a real field in model, no need to declare it as helper if it's in Meta.fields unless filtering issues.
    # But we want to customize label or queryset? keeping it in Meta is enough usually, but we declared it manually before.
    # Let's remove the manual field definition if it conflicts or keep it.
    # ModelForm will generate it. I'll remove the manual definition to avoid duplication/issues, but I need to ensure 'department' helper is valid.
    
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'filiere', 'level', 'total_hours', 'teachers']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'teachers': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inject JSON-friendly data for JS
        # Filiere -> Department mapping
        # Level -> Filieres mapping (M2M)
        
        # Note: Iterate deeply might be slow if many levels/filieres. 
        # For M2M, we need to know for each level, which filieres allow it.
        levels = Level.objects.prefetch_related('filieres').all()
        
        # We can't easily add data attributes to the widget.
        # We will assume the template iterates over queryset to build JSON.
        # But wait, the form field queryset is what matters.
        self.fields['filiere'].queryset = Filiere.objects.select_related('department').all()
        self.fields['level'].queryset = levels
        
        # Initial values for helpers
        if self.instance.pk and self.instance.filiere:
            self.initial['filiere'] = self.instance.filiere
            self.initial['department'] = self.instance.filiere.department
        # If created via helper flow, department is already set by JS potentially, but here we handle "Edit" view load.
