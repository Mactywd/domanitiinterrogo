from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('materia/<str:materia>', views.materia, name='materia'),
    path('update/', views.update, name='update'),
    path('reset/', views.reset_view, name='reset'),
    path('reset/<str:materia>', views.reset2_view, name='reset'),
    path('delete/', views.delete, name='delete')
]
