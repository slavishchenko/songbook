from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pretraga/', views.pretraga, name='pretraga'),
    path('pesmarica/', views.pesmarica, name='pesmarica'),
    path('pesmarica/rok', views.rok, name='rok-pesmarica'),
    path('pesmarica/narodno', views.narodno, name='narodna-pesmarica'),
    path('pesmarica/<str:slug>', views.izvodjac, name='izvodjac'),
    path('akordi/<int:id>/<str:izvodjac>/<str:naziv>/', views.akordi, name='akordi'),
    path('dodaj-akorde/', views.dodaj_akorde, name='dodaj-akorde'),    
]
