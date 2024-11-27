from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'domanitiinterrogo/index.html')

def manage(request):
    return render(request, 'domanitiinterrogo/manage.html')