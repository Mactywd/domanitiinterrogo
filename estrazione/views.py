from django.shortcuts import render
from firebase_admin import db
from datetime import datetime
import random
from django.http import HttpResponse
import pytz

def get_from_db(to_get):
    '''
    possible to_get: estrazioni, estrazioni/<index>
    '''

    ref = db.reference("/" + to_get)
    return ref.get()

# Create your views here.
def index(request):
    estrazioni = get_from_db("estrazioni")
    estrazioni = estrazioni[::-1]
    
    context = {
        "date": [],
        "estratti": [],
        "selected_names": [],
        "title": [],
        "estrazioni": estrazioni,
    }
    
    for estrazione in estrazioni:
        context["date"].append(estrazione["date"])
        context["estratti"].append(estrazione["estratti"])
        context["selected_names"].append(estrazione["selected_names"])
        context["title"].append(estrazione["title"])
    
    return render(request, 'estrazione/index.html', context=context)

def crea_nuova(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        selected_names = request.POST.getlist("selected_names[]")
        quantita = request.POST.get("quantita")        
        
        timezone = pytz.timezone('Europe/Rome')
        date = datetime.now(timezone).strftime('%Y-%m-%d/%H:%M')
        
        estratti = random.sample(selected_names, k=int(quantita))
        
        information = {
            "title": title,
            "selected_names": selected_names,
            "date": date,
            "estratti": estratti,
        }
        
        # ref = db.reference("/estrazioni")
        # ref.set({"estrazioni": {"temp": {"title": "Estrazione di prova", "names": ["Armini", "Bucci", "Canne"]}}})
        
        ref = db.reference("/estrazioni")
        new_index = len(get_from_db("estrazioni"))
        
        ref.child(str(new_index)).set(information)
        
        return HttpResponse(200)

def nuova(request):
    return render(request, 'estrazione/nuova.html')

def dettagli(request, estrazione_id):
    estrazione = get_from_db("estrazioni/" + str(estrazione_id))
    
    return render(request, 'estrazione/dettagli.html', context=estrazione)