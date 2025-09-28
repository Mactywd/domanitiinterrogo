from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
import markdown
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from .models import Appunto
from interrogazioni.models import Materia
from datetime import datetime
from collections import defaultdict
import json
import locale

def index(request):
    materie = Materia.objects.all().order_by("nome")
    appunti = Appunto.objects.select_related("materia").order_by("-data")

    # Per Materia → {mese: [appunti]}
    appunti_per_materia = {}
    for materia in materie:
        struttura = defaultdict(list)
        for appunto in appunti.filter(materia=materia):
            mese_nome = appunto.data.strftime("%B %Y")
            struttura[mese_nome].append(appunto)
        appunti_per_materia[materia] = dict(struttura)

    # Per Data (JSON serializzabile)
    appunti_per_data = defaultdict(list)
    for appunto in appunti:
        giorno = appunto.data.strftime("%Y-%m-%d")
        appunti_per_data[giorno].append({
            "id": appunto.id,
            "titolo": appunto.titolo,
            "materia": appunto.materia.nome,
        })

    return render(request, "appunti/index.html", {
        "materie": materie,
        "appunti_per_materia": appunti_per_materia,
        "appunti_per_data_json": json.dumps(appunti_per_data, ensure_ascii=False),
    })

@csrf_exempt
def add_appunto(request):
    if request.method == "POST":
        titolo = request.POST.get("titolo")
        materia_nome = request.POST.get("materia")
        data_str = request.POST.get("data")
        contenuto = request.POST.get("contenuto")

        if not (titolo and materia_nome and data_str and contenuto):
            return HttpResponseBadRequest("Tutti i campi sono obbligatori.")

        materia, _ = Materia.objects.get_or_create(nome=materia_nome)

        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest("Formato data non valido. Usa YYYY-MM-DD.")

        appunto = Appunto.objects.create(
            materia=materia,
            data=data,
            titolo=titolo,
            contenuto=contenuto,
        )

        if request.headers.get("Accept") == "application/json":
            return JsonResponse({
                "id": appunto.id,
                "titolo": appunto.titolo,
                "materia": appunto.materia.nome,
                "data": appunto.data.isoformat(),
                "contenuto": appunto.contenuto,
            })

        return redirect("appunti:index")

    return HttpResponseBadRequest("Metodo non supportato.")

def detail(request, pk):
    appunto = get_object_or_404(Appunto, pk=pk)

    # Conversione Markdown → HTML
    contenuto_html = mark_safe(markdown.markdown(
        appunto.contenuto,
        extensions=["extra", "tables", "fenced_code", "codehilite"]
    ))

    return render(request, "appunti/detail.html", {
        "appunto": appunto,
        "contenuto_html": contenuto_html,
    })
