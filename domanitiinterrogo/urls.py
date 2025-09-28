from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("interrogazioni/", include("interrogazioni.urls")),
    path("estrazioni/", include("estrazioni.urls")),
    path("appunti/", include("appunti.urls")),
    path("", include("home.urls")),
]
