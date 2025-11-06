from django.urls import path
from . import views

app_name = 'calendario'

urlpatterns = [
    # Main views
    path('', views.index, name='index'),
    path('unificato/', views.unified_calendar, name='unified_calendar'),
    path('materia/<int:materia_id>/', views.materia_calendar, name='materia_calendar'),

    # CRUD operations (staff only)
    path('add/', views.add_event, name='add_event'),
    path('delete/<int:evento_id>/', views.delete_event, name='delete_event'),
    path('update/<int:evento_id>/', views.update_event, name='update_event'),

    # Note editing (available to everyone)
    path('update-note/<int:evento_id>/', views.update_note, name='update_note'),

    # Shift/swap operations (staff only)
    path('materia/<int:materia_id>/shift-up/<int:evento_id>/', views.shift_up, name='shift_up'),
    path('materia/<int:materia_id>/shift-down/<int:evento_id>/', views.shift_down, name='shift_down'),
    path('materia/<int:materia_id>/insert-date/', views.insert_date, name='insert_date'),
    path('materia/<int:materia_id>/swap/', views.swap_students, name='swap_students'),
    path('materia/<int:materia_id>/bulk-shift/', views.bulk_shift_dates, name='bulk_shift_dates'),
]
