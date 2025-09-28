from django.contrib import admin
from .models import Appunto

@admin.register(Appunto)
class AppuntoAdmin(admin.ModelAdmin):
    list_display = ("materia", "data")
    list_filter = ("materia", "data")
    search_fields = ("materia__nome", "contenuto")
    date_hierarchy = "data"
