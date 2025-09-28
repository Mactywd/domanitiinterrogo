from django.db import models
from interrogazioni.models import Studente

class Estrazione(models.Model):
    titolo = models.CharField(max_length=200)  # nuovo campo
    data = models.DateTimeField(auto_now_add=True)
    studenti_estraibili = models.ManyToManyField(Studente, related_name="estrazioni_possibili")
    studenti_estratti = models.ManyToManyField(Studente, related_name="estrazioni_effettive", blank=True)

    def __str__(self):
        return f"{self.titolo} - {self.data.strftime('%d/%m/%Y %H:%M')}"
