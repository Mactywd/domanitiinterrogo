from django.db import models
from interrogazioni.models import Materia

class Appunto(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="appunti")
    data = models.DateField()
    titolo = models.CharField(max_length=200)
    contenuto = models.TextField()

    def __str__(self):
        return f"{self.titolo} - {self.materia} ({self.data})"
