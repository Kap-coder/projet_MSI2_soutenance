from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class CourseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

class CourseCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('courses:list')

class CourseUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('courses:list')

class CourseDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:list')
