from django.shortcuts import render
from firebase_admin import db


def get_from_db(to_get):
    '''
    possible to_get: estrazioni, estrazioni/<index>
    '''

    ref = db.reference("/" + to_get)
    return ref.get()

# Create your views here.
def index(request):
    estrazioni = get_from_db("estrazioni")
    #TODO
    
    return render(request, 'estrazione/index.html')


def nuova(request):
    return render(request, 'estrazione/nuova.html')