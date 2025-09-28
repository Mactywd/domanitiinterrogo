from django.contrib import admin
from .models import Materia, Studente, Interrogazione

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)

@admin.register(Studente)
class StudenteAdmin(admin.ModelAdmin):
    list_display = ("cognome",)
    search_fields = ("cognome",)

@admin.register(Interrogazione)
class InterrogazioneAdmin(admin.ModelAdmin):
    list_display = ("studente", "materia", "data")
    list_filter = ("materia", "data")
    search_fields = ("studente__cognome",)
    date_hierarchy = "data"
