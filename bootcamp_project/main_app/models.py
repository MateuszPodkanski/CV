from django.db import models
from datetime import date

class Game(models.Model):
    name = models.CharField(max_length=255)
    release_date = models.DateField(default="default")
    rating = models.DecimalField(max_digits=4, decimal_places=2)