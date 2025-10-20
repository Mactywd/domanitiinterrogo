from django.db import models
from interrogazioni.models import Studente
import json


class Estrazione(models.Model):
    titolo = models.CharField(max_length=200)
    data = models.DateTimeField(auto_now_add=True)
    studenti_estraibili = models.ManyToManyField(
        Studente, related_name="estrazioni_possibili"
    )
    studenti_estratti = models.ManyToManyField(
        Studente, related_name="estrazioni_effettive", blank=True
    )
    ordine_estratti = models.TextField(blank=True, null=True)  # stores JSON list of student IDs

    def __str__(self):
        return f"{self.titolo} - {self.data.strftime('%d/%m/%Y %H:%M')}"

    def get_studenti_estratti_in_ordine(self):
        """Return extracted students in the stored random order."""
        if not self.ordine_estratti:
            return self.studenti_estratti.all()

        try:
            ordered_ids = json.loads(self.ordine_estratti)
            # preserve order using CASE WHEN in SQL
            preserved_order = models.Case(
                *[models.When(pk=pk, then=pos) for pos, pk in enumerate(ordered_ids)]
            )
            return self.studenti_estratti.all().order_by(preserved_order)
        except Exception:
            return self.studenti_estratti.all()