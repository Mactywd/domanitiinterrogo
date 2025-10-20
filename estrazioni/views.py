from django.shortcuts import render, redirect
from .models import Estrazione
from interrogazioni.models import Studente, Materia
import random, json

def index(request):
    estrazioni = Estrazione.objects.all().order_by("-data")
    studenti = Studente.objects.all()
    # render students in alphabetical order
    studenti = studenti.order_by("cognome")
    return render(request, "estrazioni/index.html", {"estrazioni": estrazioni, "studenti": studenti})

def crea_estrazione(request):
    if request.method == "POST":
        titolo = request.POST.get("titolo")
        studenti_ids = request.POST.getlist("studenti")
        num_estratti = int(request.POST.get("num_estratti"))

        studenti_estraibili = Studente.objects.filter(id__in=studenti_ids)
        estrazione = Estrazione.objects.create(titolo=titolo)
        estrazione.studenti_estraibili.set(studenti_estraibili)

        # random draw and preserve order
        estratti = random.sample(list(studenti_estraibili), num_estratti)
        random.shuffle(estratti)

        estrazione.studenti_estratti.set(estratti)
        estrazione.ordine_estratti = json.dumps([s.id for s in estratti])
        estrazione.save()

        return redirect("estrazioni:index")


