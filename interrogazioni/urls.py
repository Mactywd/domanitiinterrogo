from django.urls import path
from . import views

app_name = "interrogazioni"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:materia_id>/", views.materia_detail, name="materia_detail"),
    path("reset/", views.reset_index, name="reset_index"),
]
