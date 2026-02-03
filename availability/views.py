from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import TeacherAvailability
from django import forms

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = TeacherAvailability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_active']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class TeacherAvailabilityListView(LoginRequiredMixin, ListView):
    model = TeacherAvailability
    template_name = 'availability/availability_list.html'
    context_object_name = 'availabilities'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.role == 'RESOURCE_MANAGER' or user.role == 'DEPARTMENT_HEAD':
            return TeacherAvailability.objects.all()
        elif user.role == 'TEACHER':
            return TeacherAvailability.objects.filter(teacher=user)
        else:
            return TeacherAvailability.objects.none()

class TeacherAvailabilityCreateView(LoginRequiredMixin, CreateView):
    model = TeacherAvailability
    form_class = AvailabilityForm
    template_name = 'availability/availability_form.html'
    success_url = reverse_lazy('availability:list')

    def form_valid(self, form):
        # Si c'est un prof, on l'assigne automatiquement
        if self.request.user.role == 'TEACHER':
            form.instance.teacher = self.request.user
        # Sinon (Admin), le champ teacher devrait être dans le formulaire si on veut qu'il puisse choisir
        # Pour l'instant, simplifions : l'admin crée pour lui-même ou on devra ajouter le champ teacher au form pour les admins
        # TODO: Gérer le cas Admin créant pour un autre prof
        if not form.instance.teacher_id:
             form.instance.teacher = self.request.user # Fallback, mais idéalement devrait être choisi
        return super().form_valid(form)

class TeacherAvailabilityUpdateView(LoginRequiredMixin, UpdateView):
    model = TeacherAvailability
    form_class = AvailabilityForm
    template_name = 'availability/availability_form.html'
    success_url = reverse_lazy('availability:list')
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
             return TeacherAvailability.objects.all()
        return TeacherAvailability.objects.filter(teacher=user)

class TeacherAvailabilityDeleteView(LoginRequiredMixin, DeleteView):
    model = TeacherAvailability
    template_name = 'availability/availability_confirm_delete.html'
    success_url = reverse_lazy('availability:list')
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
             return TeacherAvailability.objects.all()
        return TeacherAvailability.objects.filter(teacher=user)
