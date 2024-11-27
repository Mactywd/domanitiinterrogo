from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nuova', views.nuova, name='nuova'),
    path('dettagli/<int:estrazione_id>', views.dettagli, name='dettagli'),
    path('crea_nuova', views.crea_nuova, name='crea_nuova')
]