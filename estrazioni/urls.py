from django.urls import path
from . import views

app_name = "estrazioni"

urlpatterns = [
    path("", views.index, name="index"),
    path("crea/", views.crea_estrazione, name="crea"),
]
