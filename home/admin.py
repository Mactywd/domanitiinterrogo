from django.contrib import admin
from .models import MessageOfTheDay

# Register your models here.
@admin.register(MessageOfTheDay)
class MessageOfTheDayAdmin(admin.ModelAdmin):
    list_display = ("text",)