from django.shortcuts import render
from .models import Persona, Materia, LastInterrogation
from django.http import HttpResponse, HttpResponseForbidden
# redirect
from django.shortcuts import redirect
import datetime


# Create your views here.
def index(request):
    materie = Materia.objects.all()
    
    return render(request, 'interrogazioni/index.html', {'materie': materie})

def materia(request, subject):
    interrogations = LastInterrogation.objects.filter(subject__url_name=subject)
    
    return render(request, 'interrogazioni/materia.html', {'last_interrogations': interrogations, 'subject': subject})

def update(request):
    # post request
    if request.method == 'POST':
        # get data
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        
        print(name, subject, date)
        
        # get or create person
        person = Persona.objects.get(name=name)
        
        # get or create subject
        subject = Materia.objects.get(url_name=subject)
        
        # get last interrogation with this person and subject and update it
        last_interrogation = LastInterrogation.objects.filter(person=person, subject=subject).first()
        if last_interrogation:
            last_interrogation.date = date
            # use name of the month instead of number
            last_interrogation.formatted_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d %B')
            last_interrogation.color = "green"
            last_interrogation.save()
        
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
        
        # get all last interrogations with this subject and reset them
        last_interrogations = LastInterrogation.objects.filter(subject=subject)
        for last_interrogation in last_interrogations:
            last_interrogation.color = "red"
            last_interrogation.formatted_date = "mai"
            last_interrogation.save()
        
        # go to index
        return redirect('index')        
        
    else:
        return HttpResponseForbidden("Access denied")