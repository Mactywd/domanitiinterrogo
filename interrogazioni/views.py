from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from firebase_admin import db

####### UTILITY FUNCTIONS #######

def RESET_EVERYTHING(): #### DO NOT USE AS-IS
    '''
    usually just added  to the 'index' function when needed.
    temporary function, not supposed to be used indefinitely
    '''
    ref = db.reference("/")
    materie = ["Arte", "Commedia", "Filosofia", "Inglese", "Italiano", "Latino", "Matematica", "Scienze", "Storia"]
    persone = ["Armini", "Bucci", "Canne", "Cauceglia", "Cennini", "Faggioli", "Fe", "Girellini", "Lenti", "Lorenzoni", "Maione", "Montesi", "Niglio", "Polino", "Resuli", "Siebetcheu"]
    
    interrogazioni = {}
    for materia in materie:
        interrogazioni[materia] = {}
        for persona in persone:
            interrogazioni[materia][persona] = ["placeholder",]
    
    ref.set({
        'materie': materie,
        'persone': persone,
        'interrogazioni': interrogazioni
    })

def get_from_db(to_get):
    '''
    possible to_get: materie, persone, interrogazioni, interrogazioni/<materia>
    '''

    ref = db.reference("/" + to_get)
    return ref.get()

# Create your views here.
def index(request):
    
    #RESET_EVERYTHING() # normally not used, uncomment if needed
    
    materie = get_from_db("materie")
    return render(request, 'interrogazioni/index.html', {'materie': materie})

def materia(request, materia):
    interrogazioni_materia = get_from_db(f"interrogazioni/{materia}")
    
    persone = list(interrogazioni_materia.keys())
           
    interrogazioni = []
    for persona in persone:
        interrogazioni_materia_persona = list(interrogazioni_materia[persona])
        interrogazioni.append(interrogazioni_materia_persona[1:]) # first is a placeholder
        
        
    numero_interrogazioni = []
    for interrogazione in interrogazioni:
        numero_interrogazioni.append(len(interrogazione))   
    
    context = {
        'persone': persone,
        'interrogazioni': interrogazioni,
        'numero_interrogazioni': numero_interrogazioni,
        'materia': materia
    }
    
    return render(request, 'interrogazioni/materia.html', context)

def update(request):
    # post request
    if request.method == 'POST':
        # get data
        nome = request.POST.get('nome')
        materia = request.POST.get('materia')
        data = request.POST.get('data')
    
        ref = db.reference("/interrogazioni/" + materia + "/" + nome)
        interrogazioni = ref.get()
        interrogazioni.append(data)
        ref.set(interrogazioni)
        
        # reload page
        return HttpResponse("ok")
def delete(request):
    nome = request.POST.get('nome')
    materia = request.POST.get('materia')
    data = request.POST.get('data')
    
    formatted_date = ""
    if data != "NaN undefined":
        
        
        data = data.split(" ")
        
        # Month conversion
        months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        month = months.index(data[1]) + 1
        month = f"0{month}" if month < 10 else str(month)
        
        year = 2025 if int(month) < 9 else 2024
        
        day = int(data[0])
        day = f"0{day}" if day < 10 else str(day)
        
        formatted_date = f"{year}-{month}-{day}"
    
    ref = db.reference("/interrogazioni/" + materia + "/" + nome)
    interrogazioni = ref.get()
    for data in interrogazioni:
        if data in [formatted_date, ""]:
            interrogazioni.remove(data)
            ref.set(interrogazioni)
            break
    else:
        return HttpResponse(500, status=500)
    return HttpResponse("ok")


######## RESET ########
def reset_view(request):
    if request.user.is_superuser:
        materie = get_from_db("materie")      
        return render(request, 'interrogazioni/reset.html', {'materie': materie})

    else:
        return HttpResponseForbidden("Access denied")

def reset2_view(request, materia):
    if request.user.is_superuser:
        persone = get_from_db("persone")
        
        # get all last interrogations with this subject and reset them
        for persona in persone:
            ref = db.reference("/interrogazioni/" + materia + "/" + persona)
            ref.set(["placeholder",])
        
        # go to index
        return redirect('reset')        
        
    else:
        return HttpResponseForbidden("Access denied")
