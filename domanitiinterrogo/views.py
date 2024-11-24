from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'domanitiinterrogo/index.html')

def manage(request):
    return render(request, 'domanitiinterrogo/manage.html')