from django.contrib import admin
from .models import InterrogazioneProgrammata


@admin.register(InterrogazioneProgrammata)
class InterrogazioneProgrammataAdmin(admin.ModelAdmin):
    list_display = ['studente', 'materia', 'data', 'created_at']
    list_filter = ['materia', 'data']
    search_fields = ['studente__cognome', 'materia__nome']
    date_hierarchy = 'data'
