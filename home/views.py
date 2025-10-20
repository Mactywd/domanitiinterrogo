from django.shortcuts import render, redirect
from .models import MessageOfTheDay

def index(request):
    if request.method == "POST":
        text = request.POST.get("motd_text", "").strip()
        if text:
            MessageOfTheDay.objects.create(text=text)
            return redirect("home:index")  # redirect to avoid form resubmission

    motd = MessageOfTheDay.objects.order_by("?").first()
    return render(request, "home/index.html", {"motd": motd})
