from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User, Department
from enrollments.models import StudentProfile
from .forms import CustomAuthenticationForm, StudentRegistrationForm, AdminUserCreationForm, AdminUserChangeForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

@require_http_methods(["GET"])
def selection_view(request):
    """Affiche la page de sélection de compte (statique)."""
    return render(request, 'accounts/selection_cmpt.html')



# --- Mixins ---

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

# --- Auth Views ---

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vue de connexion."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.get_full_name()}!")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Identifiants invalides.")
        else:
            messages.error(request, "Erreur de connexion.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@require_http_methods(["GET", "POST"])

@require_http_methods(["GET", "POST"])
def login_student_view(request):
    """Vue de connexion dédiée aux étudiants (GET/POST)."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.get_full_name()}!")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Identifiants invalides.")
        else:
            messages.error(request, "Erreur de connexion.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login_student.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_admin_view(request):
    """Vue de connexion pour enseignants et personnel administratif."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.get_full_name()}!")
                return redirect('dashboard:home')
            else:
                messages.error(request, "Identifiants invalides.")
        else:
            messages.error(request, "Erreur de connexion.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login_admin.html', {'form': form})

def register_view(request):
    """Vue d'inscription pour les étudiants."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur
            user = form.save(commit=False)
            user.role = 'STUDENT'
            user.save()
            
            # Créer le profil étudiant
            matricule = form.cleaned_data.get('matricule')
            year = form.cleaned_data.get('year')
            department = form.cleaned_data.get('department')
            
            StudentProfile.objects.create(
                user=user,
                matricule=matricule,
                year=year,
                department=department,
                enrollment_status='PENDING'
            )
            
            messages.success(request, "Inscription réussie! Veuillez vous connecter.")
            return redirect('users:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required(login_url='users:login')
@require_http_methods(["POST"])
def logout_view(request):
    """Vue de déconnexion."""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('users:login')


# --- Department Views ---

class DepartmentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'
    paginate_by = 10

class DepartmentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Department
    template_name = 'departments/department_form.html'
    fields = ['name', 'code', 'description', 'head']
    success_url = reverse_lazy('departments:list')

class DepartmentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Department
    template_name = 'departments/department_form.html'
    fields = ['name', 'code', 'description', 'head']
    success_url = reverse_lazy('departments:list')

class DepartmentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('departments:list')


# --- User Management Views ---

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'users_manage/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.GET.get('role')
        query = self.request.GET.get('q')
        
        if role:
            queryset = queryset.filter(role=role)
        
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) | 
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_choices'] = User.ROLE_CHOICES
        context['selected_role'] = self.request.GET.get('role', '')
        context['query'] = self.request.GET.get('q', '')
        return context


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = User
    template_name = 'users_manage/user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter infos contextuelles selon le rôle
        user = self.object
        if user.role == 'STUDENT' and hasattr(user, 'student_profile'):
            context['student_profile'] = user.student_profile
        elif user.role == 'TEACHER':
            # Ajouter disponibilités ou cours enseignés si nécessaire
            pass
        elif user.role == 'DEPARTMENT_HEAD' and hasattr(user, 'headed_department'):
            context['headed_department'] = user.headed_department
        return context

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = AdminUserCreationForm
    template_name = 'users_manage/user_form.html'
    success_url = reverse_lazy('manage_users:list')

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = AdminUserChangeForm
    template_name = 'users_manage/user_form.html'
    success_url = reverse_lazy('manage_users:list')

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'users_manage/user_confirm_delete.html'
    success_url = reverse_lazy('manage_users:list')


# --- Academic Structure Views (Filiere & Level) ---
from .models import Filiere, Level
from django import forms

class FiliereListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Filiere
    template_name = 'academic/filiere_list.html'
    context_object_name = 'filieres'
    paginate_by = 10

class FiliereCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Filiere
    template_name = 'academic/filiere_form.html'
    fields = ['name', 'code', 'department', 'levels', 'description']
    success_url = reverse_lazy('academic:filiere_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['levels'].widget = forms.CheckboxSelectMultiple()
        return form

class FiliereUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Filiere
    template_name = 'academic/filiere_form.html'
    fields = ['name', 'code', 'department', 'levels', 'description']
    success_url = reverse_lazy('academic:filiere_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['levels'].widget = forms.CheckboxSelectMultiple()
        return form

class FiliereDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Filiere
    template_name = 'academic/filiere_confirm_delete.html'
    success_url = reverse_lazy('academic:filiere_list')


class LevelListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Level
    template_name = 'academic/level_list.html'
    context_object_name = 'levels'
    paginate_by = 10

class LevelCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Level
    template_name = 'academic/level_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('academic:level_list')

class LevelUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Level
    template_name = 'academic/level_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('academic:level_list')

class LevelDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Level
    template_name = 'academic/level_confirm_delete.html'
    success_url = reverse_lazy('academic:level_list')