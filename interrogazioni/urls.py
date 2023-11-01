from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('materia/<str:subject>', views.materia, name='materia'),
    path('update/', views.update, name='update'),
    path('reset/', views.reset_view, name='reset'),
    path('reset/<str:subject>', views.reset2_view, name='reset'),
]
