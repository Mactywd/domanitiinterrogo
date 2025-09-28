from django.db import models

class Materia(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Studente(models.Model):
    cognome = models.CharField(max_length=100)

    def __str__(self):
        return self.cognome


class Interrogazione(models.Model):
    studente = models.ForeignKey(Studente, on_delete=models.CASCADE, related_name="interrogazioni")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="interrogazioni")
    data = models.DateField()

    def __str__(self):
        return f"{self.studente} - {self.materia} ({self.data})"
