from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Room

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class RoomListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10

class RoomCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Room
    template_name = 'rooms/room_form.html'
    fields = ['name', 'capacity', 'room_type', 'location', 'is_available']
    success_url = reverse_lazy('rooms:list')

class RoomUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Room
    template_name = 'rooms/room_form.html'
    fields = ['name', 'capacity', 'room_type', 'location', 'is_available']
    success_url = reverse_lazy('rooms:list')

class RoomDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('rooms:list')
