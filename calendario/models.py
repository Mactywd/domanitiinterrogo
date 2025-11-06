from django.db import models
from interrogazioni.models import Studente, Materia


class InterrogazioneProgrammata(models.Model):
    """Represents a scheduled interrogation for a student in a specific subject."""
    studente = models.ForeignKey(Studente, on_delete=models.CASCADE, related_name="interrogazioni_programmate")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="interrogazioni_programmate")
    data = models.DateField()
    note = models.TextField(blank=True, null=True, help_text="Optional notes about this scheduled interrogation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data', 'materia', 'studente']
        verbose_name = "Interrogazione Programmata"
        verbose_name_plural = "Interrogazioni Programmate"

    def __str__(self):
        return f"{self.studente} - {self.materia} ({self.data})"
