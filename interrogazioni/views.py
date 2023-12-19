from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
import datetime
from firebase_admin import db
import json

# Create your views here.
def index(request):
    ref = db.reference("/")
    materie = ref.get().keys()
    materie = list(materie)
    
    url_materie = []
    
    for materia in materie:
        url_materie.append(materia.replace(" ", "_").lower())
    
    
    #### TEMPORARY ####
    # # reset everything
    # for subject in materie:
    #     for persona in Persona.objects.all():
    #         ref = db.reference("/" + subject.name + "/" + persona.name)
    #         ref.set({"placeholder": 0})
    
    return render(request, 'interrogazioni/index.html', {'materie': zip(materie, url_materie)})

def materia(request, subject):
    name = subject.replace("_", " ").title()
    ref = db.reference("/" + name)
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
        
        sub_name = subject.replace("_", " ").title()
        ref = db.reference("/" + sub_name + "/" + name)
        print(ref.path)
        
        ref.push(date)
        
        # reload page
        return HttpResponse("ok")


def reset_view(request):
    if request.user.is_superuser:
        ref = db.reference("/")
        materie = ref.get().keys()
        materie = list(materie)

        url_materie = []    
        for materia in materie:
            url_materie.append(materia.replace(" ", "_").lower())
        
    
        return render(request, 'interrogazioni/reset.html', {'materie': zip(materie, url_materie)})

    else:
        return HttpResponseForbidden("Access denied")

def reset2_view(request, subject):
    if request.user.is_superuser:
        # get subject
        real_name = subject.replace("_", " ").title()
        
        ref = db.reference("/" + real_name)
        people = ref.get().keys()
        people = list(people)
        ref.set({})
        
        # get all last interrogations with this subject and reset them
        for persona in people:
            ref = db.reference("/" + real_name + "/" + persona)
            ref.set({"placeholder": 0})
        
        # go to index
        return redirect('index')        
        
    else:
        return HttpResponseForbidden("Access denied")