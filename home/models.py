from django.db import models

class MessageOfTheDay(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]
