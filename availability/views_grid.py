from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import TeacherAvailability
from schedules.models import GlobalTimeSlot
import datetime

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'TEACHER'

class AvailabilityGridView(LoginRequiredMixin, TeacherRequiredMixin, View):
    template_name = 'availability/availability_grid.html'

    def get(self, request):
        # Récupérer tous les créneaux globaux, triés
        global_slots = GlobalTimeSlot.objects.filter(is_break=False).order_by('day_of_week', 'start_time')
        
        # Grouper par jour
        grouped_slots = {}
        for slot in global_slots:
            if slot.day_of_week not in grouped_slots:
                grouped_slots[slot.day_of_week] = []
            grouped_slots[slot.day_of_week].append(slot)
            
        # Récupérer les disponibilités existantes de l'enseignant (seulement celles sans date ou actives)
        # Pour simplifier l'édition "Matrice", on ne charge que celles qui correspondent exactement aux slots globaux ?
        # Ou on fait une approximation.
        
        existing_availabilities = TeacherAvailability.objects.filter(teacher=request.user)
        
        # Créer un set de clés "jour_start_end" pour vérification rapide
        active_slots_keys = set()
        for avail in existing_availabilities:
            # On considère actif si au moins overlap ? Pour l'instant : correspondance stricte ou inclusion
            # Clé simple : jour_heuredebut
            key = f"{avail.day_of_week}_{avail.start_time.strftime('%H:%M:%S')}"
            active_slots_keys.add(key)

        context = {
            'grouped_slots': grouped_slots,
            'days_display': dict(GlobalTimeSlot._meta.get_field('day_of_week').choices),
            'active_slots_keys': active_slots_keys,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Données reçues : une liste de 'slots' cochés
        # Format attendu : "day_start_end" (ex: "0_08:00:00_10:00:00")
        
        selected_slots = request.POST.getlist('selected_slots')
        
        # Optionnel : Dates de validité pour ce lot
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if not start_date: start_date = None
        if not end_date: end_date = None
        
        # Stratégie :
        # 1. Supprimer les disponibilités existantes qui correspondaient à des GlobalTimeSlots (pour éviter doublons/conflits lors d'une mise à jour complète)
        # SAUF si on gère des périodes différentes.
        # Pour l'instant : On supprime tout ce qui n'a pas de date (permanent) si on ne spécifie pas de date.
        # Si on spécifie une date, on crée sans supprimer les anciennes (complexité++).
        
        # Simplification v1 : Mode "Ma semaine type". On écrase la semaine type précédente (celle sans dates).
        if not start_date and not end_date:
            TeacherAvailability.objects.filter(teacher=request.user, start_date__isnull=True, end_date__isnull=True).delete()
        
        count = 0
        for item in selected_slots:
            try:
                day, start, end = item.split('_')
                # Création
                TeacherAvailability.objects.create(
                    teacher=request.user,
                    day_of_week=int(day),
                    start_time=start,
                    end_time=end,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True
                )
                count += 1
            except ValueError:
                continue
                
        messages.success(request, f"{count} créneaux de disponibilité enregistrés.")
        return redirect('availability:grid')
