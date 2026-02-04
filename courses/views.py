from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Course
from .forms import CourseForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'TEACHER'

# --- Admin Views ---

class CourseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

class CourseDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

class CourseCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:list')

class CourseUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:list')

class CourseDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:list')


# --- Teacher Views ---

class TeacherCourseListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Course
    template_name = 'courses/teacher_course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        # Filter courses where the current user is in the teachers list
        return Course.objects.filter(teachers=self.request.user)

class TeacherCourseDetailView(LoginRequiredMixin, TeacherRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/teacher_course_detail.html'
    context_object_name = 'course'
    
    def get_queryset(self):
        # Ensure teacher can only view their own courses details
        return Course.objects.filter(teachers=self.request.user)
