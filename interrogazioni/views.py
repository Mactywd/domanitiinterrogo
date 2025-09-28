from django.shortcuts import render, get_object_or_404, redirect
from .models import Materia, Studente, Interrogazione
from django.db.models import Max
from django.utils.dateparse import parse_date
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    materie = Materia.objects.all().order_by("nome")
    return render(request, "interrogazioni/index.html", {"materie": materie})


def materia_detail(request, materia_id):
    materia = get_object_or_404(Materia, pk=materia_id)


    if request.method == "POST":
        studente_id = request.POST.get("studente_id")
        data_str = request.POST.get("data")
        remove_id = request.POST.get("remove_id")

        if studente_id and data_str:
            if remove_id:
                interrogazione = get_object_or_404(Interrogazione, pk=remove_id)
                interrogazione.delete()
                return redirect("interrogazioni:materia_detail", materia_id=materia.id)
            
            studente = get_object_or_404(Studente, pk=studente_id)
            data = parse_date(data_str)

            # Aggiunge nuova interrogazione solo se non esiste già
            exists = Interrogazione.objects.filter(
                studente=studente, materia=materia, data=data
            ).exists()
            if not exists:
                Interrogazione.objects.create(
                    studente=studente,
                    materia=materia,
                    data=data
                )

        return redirect("interrogazioni:materia_detail", materia_id=materia.id)

    # Costruiamo i dati per ogni studente
    studenti_data = []
    studenti = Studente.objects.all().order_by("cognome")

    for studente in studenti:
        interrogazioni = Interrogazione.objects.filter(studente=studente, materia=materia)
        count = interrogazioni.count()
        ultima = interrogazioni.aggregate(Max("data"))["data__max"]

        studenti_data.append({
            "studente": studente,
            "count": count,
            "ultima": ultima
        })

    return render(request, "interrogazioni/materia_detail.html", {
        "materia": materia,
        "studenti_data": studenti_data
    })

@staff_member_required
def reset_index(request):
    materie = Materia.objects.all().order_by("nome")

    if request.method == "POST":
        materia_id = request.POST.get("materia_id")
        materia = get_object_or_404(Materia, pk=materia_id)

        # elimina tutte le interrogazioni della materia
        Interrogazione.objects.filter(materia=materia).delete()

        return redirect("interrogazioni:reset_index")

    return render(request, "interrogazioni/reset_index.html", {"materie": materie})