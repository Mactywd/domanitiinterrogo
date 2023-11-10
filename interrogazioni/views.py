from django.shortcuts import render
from .models import Persona, Materia, LastInterrogation
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
import datetime
from firebase_admin import db
import json

# Create your views here.
def index(request):
    materie = Materia.objects.all()
    
    #### TEMPORARY ####
    # # reset everything
    # for subject in materie:
    #     for persona in Persona.objects.all():
    #         ref = db.reference("/" + subject.name + "/" + persona.name)
    #         ref.set({"placeholder": 0})
    
    return render(request, 'interrogazioni/index.html', {'materie': materie})

def materia(request, subject):
    subject = Materia.objects.get(url_name=subject)
    ref = db.reference("/" + subject.name)
    interrogated = ref.get()
    
    people = list(interrogated.keys())
    interrogations = list(interrogated.values())
    for i in range(len(interrogations)):
        # interrogations[i] = {"placeholder": 0, "jn77tGGUh--": "2021-10-10"}
        # remove placeholder
        interrogations[i].pop("placeholder")
        
        
        
    interrogated_times = []
    for interrogation in interrogations:
        interrogated_times.append(len(interrogation))   
    
    context = {
        'people': people,
        'interrogations': interrogations,
        'interrogated_times': interrogated_times,
        'subject': subject,
    }
    
    return render(request, 'interrogazioni/materia.html', context)

def update(request):
    # post request
    if request.method == 'POST':
        # get data
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        
        print(name, subject, date)
        person = Persona.objects.get(name=name)
        subject = Materia.objects.get(name=subject)
        
        ref = db.reference("/" + subject.name + "/" + person.name)
        ref.push(date)
        
        # reload page
        return HttpResponse("ok")


def reset_view(request):
    if request.user.is_superuser:
        materie = Materia.objects.all()
    
        return render(request, 'interrogazioni/reset.html', {'materie': materie})

    else:
        return HttpResponseForbidden("Access denied")

def reset2_view(request, subject):
    if request.user.is_superuser:
        # get subject
        subject = Materia.objects.get(url_name=subject)
        
        ref = db.reference("/" + subject.name)
        ref.set({})
        # get all last interrogations with this subject and reset them
        for persona in Persona.objects.all():
            ref = db.reference("/" + subject.name + "/" + persona.name)
            ref.set({"placeholder": 0})
        
        # go to index
        return redirect('index')        
        
    else:
        return HttpResponseForbidden("Access denied")