from django.contrib import admin
from .models import Estrazione

@admin.register(Estrazione)
class EstrazioneAdmin(admin.ModelAdmin):
    list_display = ("data",)
    filter_horizontal = ("studenti_estraibili",)
    date_hierarchy = "data"
