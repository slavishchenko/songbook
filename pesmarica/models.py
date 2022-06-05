from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Izvodjac(models.Model):
    ime = models.CharField(max_length=250)

    def __str__(self):
        return self.ime
class Album(models.Model):
    naziv_albuma = models.CharField(max_length=250)
    izvodjac = models.ForeignKey(Izvodjac, on_delete=models.CASCADE)

    def __str__(self):
        return self.naziv_albuma
class Pesma(models.Model):
    CHOICES = (
        ('Za početnike', 'Za početnike'),
        ('Srednje', 'Srednje'),
        ('Teško', 'Teško')
    )

    naziv_pesme = models.CharField(max_length=100)
    izvodjac = models.ForeignKey(Izvodjac, on_delete=models.CASCADE)
    zanr = models.CharField(max_length=30)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    tonalitet = models.CharField(max_length=3)
    takt = models.CharField(max_length=10)
    tempo = models.IntegerField()
    ritam = models.CharField(max_length=30)
    
    sekcije = models.CharField(max_length=50)
    forspil = models.TextField()
    strofa = models.TextField()
    predrefren = models.TextField(blank=True, null=True)
    refren = models.TextField()
    drugo = models.TextField(blank=True, null=True)
    aranzman = models.CharField(max_length=100)

    tezina = models.CharField(max_length=12, choices=CHOICES, default='Za početnike')
    odobrio_admin = models.BooleanField(default=False)

    datum_dodavanja = models.DateTimeField(default=timezone.now)
    dodao = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.naziv_pesme

