from django.db import models
from django.contrib.auth.models import User
from pesmarica.models import Pesma
from django.utils import timezone
from django.urls import reverse

#* Custom Functions
def slugify(string):
    try:
        string = string.lower().split()
        string = '-'.join(string)
        return string
    except:
        string = string.lower()
        return string

#* END CUSTOM

class Repertoar(models.Model):
    naslov = models.CharField(max_length=100)
    opis = models.TextField()
    set = models.ManyToManyField(Pesma)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    javno = models.BooleanField(default=True)
    datum_dodavanja = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.naslov.title()

    def get_absolute_url(self):
        return reverse('repertoar-detail', kwargs={'pk': self.pk, 'slug': slugify(self.naslov)})


