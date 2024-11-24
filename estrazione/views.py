from django.shortcuts import render
from firebase_admin import db

# Create your views here.
def index(request):
    return render(request, 'estrazione/index.html')