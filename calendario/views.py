from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from interrogazioni.models import Materia, Studente
from .models import InterrogazioneProgrammata


def index(request):
    """Display all subjects with count of scheduled interrogations."""
    materie = Materia.objects.all().order_by("nome")

    # Add count of scheduled interrogations for each subject
    materie_data = []
    for materia in materie:
        count = InterrogazioneProgrammata.objects.filter(materia=materia).count()
        materie_data.append({
            'materia': materia,
            'count': count
        })

    return render(request, "calendario/index.html", {
        "materie_data": materie_data
    })


def materia_calendar(request, materia_id):
    """Display scheduled interrogations for a specific subject."""
    materia = get_object_or_404(Materia, pk=materia_id)

    # Get all scheduled interrogations for this subject, ordered by date
    eventi = InterrogazioneProgrammata.objects.filter(
        materia=materia
    ).select_related('studente').order_by('data')

    # Get all students for the add form
    studenti = Studente.objects.all().order_by("cognome")

    return render(request, "calendario/materia_calendar.html", {
        "materia": materia,
        "eventi": eventi,
        "studenti": studenti
    })


def unified_calendar(request):
    """Display all scheduled interrogations across all subjects."""
    # Get all events ordered by date
    eventi = InterrogazioneProgrammata.objects.all().select_related(
        'studente', 'materia'
    ).order_by('data')

    # Group by date
    from collections import defaultdict
    eventi_per_data = defaultdict(list)

    for evento in eventi:
        data_str = evento.data.strftime("%Y-%m-%d")
        eventi_per_data[data_str].append(evento)

    # Convert to sorted list of tuples
    eventi_grouped = sorted(eventi_per_data.items())

    return render(request, "calendario/unified_calendar.html", {
        "eventi_grouped": eventi_grouped
    })


@staff_member_required
@require_POST
def add_event(request):
    """Add a new scheduled interrogation."""
    materia_id = request.POST.get("materia_id")
    studente_id = request.POST.get("studente_id")
    data_str = request.POST.get("data")
    note = request.POST.get("note", "")

    if materia_id and studente_id and data_str:
        materia = get_object_or_404(Materia, pk=materia_id)
        studente = get_object_or_404(Studente, pk=studente_id)
        data = parse_date(data_str)

        # Create the event
        InterrogazioneProgrammata.objects.create(
            studente=studente,
            materia=materia,
            data=data,
            note=note
        )

    return redirect("calendario:materia_calendar", materia_id=materia_id)


@staff_member_required
@require_POST
def delete_event(request, evento_id):
    """Delete a scheduled interrogation."""
    evento = get_object_or_404(InterrogazioneProgrammata, pk=evento_id)
    materia_id = evento.materia.id
    evento.delete()

    return redirect("calendario:materia_calendar", materia_id=materia_id)


@staff_member_required
@require_POST
def update_event(request, evento_id):
    """Update an existing scheduled interrogation (admin only - updates date and notes)."""
    evento = get_object_or_404(InterrogazioneProgrammata, pk=evento_id)

    data_str = request.POST.get("data")
    note = request.POST.get("note")

    if data_str:
        evento.data = parse_date(data_str)
    if note is not None:
        evento.note = note

    evento.save()

    return redirect("calendario:materia_calendar", materia_id=evento.materia.id)


@require_POST
def update_note(request, evento_id):
    """Update only the notes of an interrogation (available to everyone)."""
    evento = get_object_or_404(InterrogazioneProgrammata, pk=evento_id)

    note = request.POST.get("note")
    if note is not None:
        evento.note = note
        evento.save()

    return redirect("calendario:materia_calendar", materia_id=evento.materia.id)


@staff_member_required
@require_POST
def shift_up(request, materia_id, evento_id):
    """Shift a student's date one position earlier (swap with previous student)."""
    materia = get_object_or_404(Materia, pk=materia_id)
    evento = get_object_or_404(InterrogazioneProgrammata, pk=evento_id, materia=materia)

    # Get all events for this materia ordered by date
    eventi = list(InterrogazioneProgrammata.objects.filter(
        materia=materia
    ).order_by('data'))

    # Find the index of this event
    try:
        index = eventi.index(evento)
        if index > 0:
            # Swap dates with previous event
            prev_evento = eventi[index - 1]
            evento.data, prev_evento.data = prev_evento.data, evento.data
            evento.save()
            prev_evento.save()
    except ValueError:
        pass

    return redirect("calendario:materia_calendar", materia_id=materia_id)


@staff_member_required
@require_POST
def shift_down(request, materia_id, evento_id):
    """Shift a student's date one position later (swap with next student)."""
    materia = get_object_or_404(Materia, pk=materia_id)
    evento = get_object_or_404(InterrogazioneProgrammata, pk=evento_id, materia=materia)

    # Get all events for this materia ordered by date
    eventi = list(InterrogazioneProgrammata.objects.filter(
        materia=materia
    ).order_by('data'))

    # Find the index of this event
    try:
        index = eventi.index(evento)
        if index < len(eventi) - 1:
            # Swap dates with next event
            next_evento = eventi[index + 1]
            evento.data, next_evento.data = next_evento.data, evento.data
            evento.save()
            next_evento.save()
    except ValueError:
        pass

    return redirect("calendario:materia_calendar", materia_id=materia_id)


@staff_member_required
@require_POST
def insert_date(request, materia_id):
    """Insert a new date and shift all subsequent events one position later."""
    materia = get_object_or_404(Materia, pk=materia_id)

    studente_id = request.POST.get("studente_id")
    data_str = request.POST.get("data")

    if studente_id and data_str:
        studente = get_object_or_404(Studente, pk=studente_id)
        new_data = parse_date(data_str)

        # Get all events after this date
        eventi_dopo = InterrogazioneProgrammata.objects.filter(
            materia=materia,
            data__gte=new_data
        ).order_by('data')

        # Store the dates to shift
        date_shifts = []
        for evento in eventi_dopo:
            date_shifts.append(evento.data)

        # Create new event
        InterrogazioneProgrammata.objects.create(
            studente=studente,
            materia=materia,
            data=new_data
        )

        # Shift all subsequent events by one day
        # This is a simple approach; you might want a more sophisticated date shifting
        if date_shifts:
            eventi_dopo_list = list(eventi_dopo)
            for i, evento in enumerate(eventi_dopo_list):
                if i < len(date_shifts) - 1:
                    evento.data = date_shifts[i + 1]
                else:
                    # For the last event, add one day
                    evento.data = date_shifts[i] + timedelta(days=1)
                evento.save()

    return redirect("calendario:materia_calendar", materia_id=materia_id)


@staff_member_required
@require_POST
def swap_students(request, materia_id):
    """Swap the dates of two students."""
    materia = get_object_or_404(Materia, pk=materia_id)

    evento1_id = request.POST.get("evento1_id")
    evento2_id = request.POST.get("evento2_id")

    if evento1_id and evento2_id:
        evento1 = get_object_or_404(InterrogazioneProgrammata, pk=evento1_id, materia=materia)
        evento2 = get_object_or_404(InterrogazioneProgrammata, pk=evento2_id, materia=materia)

        # Swap dates
        evento1.data, evento2.data = evento2.data, evento1.data
        evento1.save()
        evento2.save()

    return redirect("calendario:materia_calendar", materia_id=materia_id)


@staff_member_required
@require_POST
def bulk_shift_dates(request, materia_id):
    """
    Bulk shift interrogations after a certain date.

    Two modes:
    - 'forward': Shift all interrogations after start_date forward by one position.
      The last interrogation will be moved to a new date (overflow_date).
      Use this when you need to skip a date (e.g., interrogations can't happen on that day).

    - 'backward': Fill in a new available date by shifting subsequent interrogations backward.
      Example: If you have interrogations on 20th, 22nd, 25th and a new date 15th opens up,
      all interrogations after 15th shift back: 20th→15th, 22nd→20th, 25th→22nd.
      This leaves the last date slot (25th) empty and available for future use.
    """
    materia = get_object_or_404(Materia, pk=materia_id)

    direction = request.POST.get("direction")  # 'forward' or 'backward'
    start_date_str = request.POST.get("start_date")
    overflow_date_str = request.POST.get("overflow_date")  # Only for forward shift

    if not direction or not start_date_str:
        return redirect("calendario:materia_calendar", materia_id=materia_id)

    start_date = parse_date(start_date_str)

    if direction == 'forward':
        # Get all events for this materia after (and including) start_date, ordered by date
        eventi = list(InterrogazioneProgrammata.objects.filter(
            materia=materia,
            data__gte=start_date
        ).order_by('data'))

        if not eventi:
            return redirect("calendario:materia_calendar", materia_id=materia_id)

        # Shift forward: each event takes the date of the next event
        # The last event goes to overflow_date
        if overflow_date_str:
            overflow_date = parse_date(overflow_date_str)
        else:
            # If no overflow date specified, add 7 days to the last date
            overflow_date = eventi[-1].data + timedelta(days=7)

        # Extract all dates
        dates = [e.data for e in eventi]
        dates.append(overflow_date)  # Add the overflow date at the end

        # Shift: each event gets the next date
        for i in range(len(eventi) - 1, -1, -1):
            eventi[i].data = dates[i + 1]
            eventi[i].save()

    elif direction == 'backward':
        # Get all events AFTER start_date (not including it)
        # start_date is the new available date that we want to fill
        eventi = list(InterrogazioneProgrammata.objects.filter(
            materia=materia,
            data__gt=start_date
        ).order_by('data'))

        if not eventi:
            return redirect("calendario:materia_calendar", materia_id=materia_id)

        # Extract all dates starting with the new available date
        # dates[i] will be the old date of eventi[i-1] (or start_date for i=0)
        dates = [start_date] + [e.data for e in eventi[:-1]]

        # Shift backward: each event gets the previous date in sequence
        # First event gets start_date, second gets old first date, etc.
        # This leaves the last date slot empty (available for future use)
        for i in range(len(eventi)):
            eventi[i].data = dates[i]
            eventi[i].save()

    return redirect("calendario:materia_calendar", materia_id=materia_id)
