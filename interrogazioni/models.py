from django.db import models
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.
    
class Persona(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Materia(models.Model):
    name = models.CharField(max_length=50)
    url_name = models.CharField(max_length=50, default="")
    
    def __str__(self):
        return self.name

@receiver(pre_save, sender=Materia)
def _post_save_receiver(sender, instance, *args, **kwargs):
    if instance.name:
        instance.url_name = instance.name.split(" ")[-1].lower()


class LastInterrogation(models.Model):
    person = models.ForeignKey(Persona, on_delete=models.CASCADE)
    subject = models.ForeignKey(Materia, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime(2000, 1, 1, 0, 0, 0))
    color = models.CharField(max_length=50, default="red")
    formatted_date = models.CharField(max_length=50, default="mai")
    
    def __str__(self):
        return self.person.name + ' ' + self.subject.name + ' ' + self.date.strftime('%d/%m/%Y %H:%M:%S')