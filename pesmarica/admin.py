from django.contrib import admin
from .models import Album, Izvodjac, Pesma

admin.site.register(Izvodjac)
admin.site.register(Album)
admin.site.register(Pesma)