from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'interrogazioni/index.html')

def materia(request):
    return render(request, 'interrogazioni/materia.html')