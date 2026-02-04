from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import datetime

from .models import GlobalTimeSlot
from .forms import GlobalTimeSlotForm, ScheduleGeneratorForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class GlobalTimeSlotListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = GlobalTimeSlot
    template_name = 'schedules/global_timeslot_list.html'
    context_object_name = 'slots'
    ordering = ['day_of_week', 'start_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group by day for easier display
        grouped_slots = {}
        for slot in self.get_queryset():
            if slot.get_day_of_week_display() not in grouped_slots:
                grouped_slots[slot.get_day_of_week_display()] = []
            grouped_slots[slot.get_day_of_week_display()].append(slot)
        context['grouped_slots'] = grouped_slots
        return context

class GlobalTimeSlotCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = GlobalTimeSlot
    form_class = GlobalTimeSlotForm
    template_name = 'schedules/global_timeslot_form.html'
    success_url = reverse_lazy('schedules:list')

class GlobalTimeSlotUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = GlobalTimeSlot
    form_class = GlobalTimeSlotForm
    template_name = 'schedules/global_timeslot_form.html'
    success_url = reverse_lazy('schedules:list')

class GlobalTimeSlotDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = GlobalTimeSlot
    template_name = 'schedules/global_timeslot_confirm_delete.html'
    success_url = reverse_lazy('schedules:list')

class ScheduleGeneratorView(LoginRequiredMixin, AdminRequiredMixin, FormView):
    template_name = 'schedules/generator_form.html'
    form_class = ScheduleGeneratorForm
    success_url = reverse_lazy('schedules:list')

    def form_valid(self, form):
        days = form.cleaned_data['days']
        start_time = form.cleaned_data['day_start_time']
        end_time = form.cleaned_data['day_end_time']
        slot_duration = form.cleaned_data['slot_duration']
        break_duration = form.cleaned_data['break_duration']
        
        # Logic to generate slots
        # Convert times to simplified minutes from midnight for calculation
        start_min = start_time.hour * 60 + start_time.minute
        end_min = end_time.hour * 60 + end_time.minute
        
        generated_count = 0
        
        # DELETE existing slots for the selected days to ensure a fresh generation
        # conversion of string days from form to integers
        days_ints = [int(d) for d in days]
        GlobalTimeSlot.objects.filter(day_of_week__in=days_ints).delete()
        
        for day in days:
            current_time = start_min
            
            while current_time + slot_duration <= end_min:
                # Slot start and end
                s_hour, s_min = divmod(current_time, 60)
                e_hour, e_min = divmod(current_time + slot_duration, 60)
                
                slot_start = datetime.time(s_hour, s_min)
                slot_end = datetime.time(e_hour, e_min)
                
                # Create Course Slot
                GlobalTimeSlot.objects.get_or_create(
                    day_of_week=int(day),
                    start_time=slot_start,
                    end_time=slot_end,
                    defaults={'is_break': False}
                )
                generated_count += 1
                
                current_time += slot_duration
                
                # Add Break if not end of day
                if current_time + break_duration <= end_min and break_duration > 0:
                    # Break start and end
                    bs_hour, bs_min = divmod(current_time, 60)
                    be_hour, be_min = divmod(current_time + break_duration, 60)
                    
                    break_start = datetime.time(bs_hour, bs_min)
                    break_end = datetime.time(be_hour, be_min)
                    
                    GlobalTimeSlot.objects.get_or_create(
                         day_of_week=int(day),
                         start_time=break_start,
                         end_time=break_end,
                         defaults={'is_break': True}
                    )
                    
                    current_time += break_duration

        messages.success(self.request, f"{generated_count} créneaux de cours générés avec succès.")
        return super().form_valid(form)
