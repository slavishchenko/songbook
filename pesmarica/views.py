from django.core.paginator import Paginator
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from repertoar.models import Repertoar
from .models import Album, Izvodjac, Pesma
from django.utils.html import escape
from django.db.models import Q
from .forms import AlbumForm, IzvodjacForm, PesmaForm
from django.contrib import messages


def index(request):
    user_id = request.user.id
    repertoari = Repertoar.objects.filter(autor_id=user_id)
    najnovije = Pesma.objects.filter(odobrio_admin=True).order_by('datum_dodavanja').reverse()[:10]

    sve_pesme = list(Pesma.objects.all().filter(odobrio_admin=True))
    try:
        nasumicno = random.sample(sve_pesme, 10)
    except:
        nasumicno = random.sample(sve_pesme, len(sve_pesme))

    za_pocetnike = Pesma.objects.filter(odobrio_admin=True, tezina='Za početnike').order_by('datum_dodavanja').reverse()[:10]

    context = {
        'najnovije': najnovije,
        'nasumicno': nasumicno,
        'pocetnicke': za_pocetnike,
        'repertoari': repertoari
    }
    return render(request, 'pesmarica/index.html', context)

def pesmarica(request):

    izvodjaci = Izvodjac.objects.get_queryset().order_by('id')

    paginator = Paginator(izvodjaci, 16) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    najnovije = Pesma.objects.filter(odobrio_admin=True).order_by('datum_dodavanja').exclude(dodao_id=request.user.id).reverse()[:5]

    title = 'Zbirka Pesama | Pesmarica'

    context = {
        'page_obj': page_obj,
        'najnovije': najnovije,
        'title': title      
    }

    return render(request, 'pesmarica/pesmarica.html', context)

def rok(request):

    izvodjaci = []

    pesme = Pesma.objects.all().filter(odobrio_admin=True).filter(zanr='Rok')
    for p in pesme:
        if p.izvodjac not in izvodjaci:
            izvodjaci.append(p.izvodjac)

    paginator = Paginator(izvodjaci, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    najnovije = Pesma.objects.filter(odobrio_admin=True).filter(zanr__icontains='rok').order_by('datum_dodavanja').exclude(dodao_id=request.user.id).reverse()[:10]
    
    title = 'Zbirka Pesama | Rok pesmarica'

    context = {
        'page_obj': page_obj,
        'najnovije': najnovije[:5],
        'title': title
    }

    return render(request, 'pesmarica/rok.html', context)

def narodno(request):

    izvodjaci = []

    pesme = Pesma.objects.all().filter(odobrio_admin=True).values()
    for pesma in pesme:
        if pesma['zanr'].lower() == 'narodno':
            izvodjac_obj = Izvodjac.objects.filter(id=pesma['izvodjac_id'])
            if izvodjac_obj[0] not in izvodjaci:
                izvodjaci.append(izvodjac_obj[0])
            else:
                pass

    paginator = Paginator(izvodjaci, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    najnovije = []
    najnovije = Pesma.objects.filter(odobrio_admin=True).filter(zanr__icontains='narodno').order_by('datum_dodavanja').exclude(dodao_id=request.user.id).reverse()[:10]

    title = 'Zbirka Pesama | Narodna pesmarica'

    context = {
        'page_obj': page_obj,
        'najnovije': najnovije[:5],
        'title': title
    }

    return render(request, 'pesmarica/narodno.html', context)


def pretraga(request):
    user_id = request.user.id
    repertoari = Repertoar.objects.filter(autor_id=user_id)
    #! Pretraga ne radi u potpunosti sa SQlite bazom
    if request.method == 'GET':

        q = escape(request.GET['q'])
        pesme = Pesma.objects.filter(odobrio_admin=True).filter(Q(naziv_pesme__icontains=q) | Q(izvodjac__ime__icontains=q))

        najnovije = Pesma.objects.filter(odobrio_admin=True).order_by('datum_dodavanja').reverse()[:10]

        title = 'Zbirka Pesama | Pretraga'

        context = {
            'q': q,
            'pesme': pesme,
            'najnovije': najnovije,
            'title': title,
            'repertoari': repertoari
        }

        return render(request, 'pesmarica/pretraga.html', context)
    else:
        return render(request, 'pesmarica/pretraga.html')

def izvodjac(request, slug):
    slug = slug.split('-')
    slug  = ' '.join(slug)

    user_id = request.user.id
    repertoari = Repertoar.objects.filter(autor_id=user_id)

    izvodjac_obj = Izvodjac.objects.filter(ime__icontains=slug)
    for field in izvodjac_obj:
        id = field.id
    
    pesme = Pesma.objects.filter(odobrio_admin=True).filter(izvodjac=id)

    albumi = Album.objects.filter(izvodjac=id)

    najnovije = Pesma.objects.filter(odobrio_admin=True).filter(izvodjac=id).exclude(dodao_id=request.user.id).reverse()[:5]

    title = f'Zbirka Pesama | {slug.title()}'

    context = {
        'slug': slug,
        'pesme': pesme,
        'albumi': albumi,
        'najnovije': najnovije,
        'repertoari': repertoari,
        'title': title
    }
    return render(request, 'pesmarica/izvodjac.html', context)

def akordi(request, id, izvodjac, naziv):

    def split(word):
        return list(word)

    try:
        izvodjac = izvodjac.split('-')
        izvodjac = ' '.join(izvodjac)
        naziv = naziv.split('-')
        naziv = ' '.join(naziv)
    except:
        pass

    ### ARANZMAN
    pesma = Pesma.objects.filter(odobrio_admin=True).filter(id=id)
    for p in pesma:
        aranzman = p.aranzman

    aranzman = aranzman.split(',')
    ### ARANZMAN KRAJ

    ### AKORDI
        # SEKCIJE #
    for x in pesma:
        sekcija = x.sekcije
        sekcije = sekcija.split(', ')

    for s in pesma:
        forspil = s.forspil
        strofa = s.strofa.splitlines()
        refren = s.refren.splitlines()
        predrefren = s.predrefren.splitlines()
        drugo = s.drugo.splitlines()
        autor = s.dodao
    ### AKORDI KRAJ

    ### NAJNOVIJE OD IZVODJACA
    izvodjac_obj = Izvodjac.objects.filter(ime__icontains=izvodjac)
    for i in izvodjac_obj:
        izvodjac_id = i.id
    najnovije_pesme = []
    pesme_od_izvodjaca = Pesma.objects.filter(odobrio_admin=True).filter(izvodjac_id=izvodjac_id).exclude(dodao_id=request.user.id).exclude(id=id).order_by('datum_dodavanja').reverse()[:5]
    #* REPERTOARI *#
    try:
        repertoari = Repertoar.objects.filter(autor=request.user)
    except:
        repertoari = []

    title = f'{izvodjac.title()} - {naziv.title()}'
    context = {
        'izvodjac': izvodjac,
        'naziv': naziv,
        'pesma': pesma,
        'aranzman': aranzman,
        'najnovije_pesme': najnovije_pesme,
        'sekcije': sekcije,
        'forspil': forspil,
        'strofa': strofa,
        'predrefren': predrefren,
        'refren': refren,
        'drugo': drugo,
        'autor': autor,
        'pesme_od_izvodjaca': pesme_od_izvodjaca,
        'repertoari': repertoari,
        'title': title
    }

    return render(request, 'pesmarica/akordi.html', context)

@login_required
def dodaj_akorde(request):

    if request.method == 'POST':
        
        izvodjac_form = IzvodjacForm(request.POST)
        album_form = AlbumForm(request.POST)
        pesma_form = PesmaForm(request.POST)

        user = request.user

        if izvodjac_form.is_valid() and album_form.is_valid() and pesma_form.is_valid():
            # IZVODJAC
            izvodjac_ime = request.POST['ime']
            if not Izvodjac.objects.filter(ime__icontains=izvodjac_ime):
                izvodjac = Izvodjac(ime=izvodjac_ime)
                izvodjac.save()
            else:
                izvodjac_obj = Izvodjac.objects.filter(ime__icontains=izvodjac_ime)
                for f in izvodjac_obj:
                    izvodjac = f
                izvodjac_form = IzvodjacForm(instance=izvodjac)
            # ALBUM
            naziv_albuma = request.POST['naziv_albuma']
            if not Album.objects.filter(naziv_albuma__icontains=naziv_albuma):
                album = album_form.save(commit=False)
                album.izvodjac = izvodjac
                album.save()
            else:
                album_obj = Album.objects.filter(naziv_albuma__icontains=naziv_albuma)
                for a in album_obj:
                    album = a
                album_form = AlbumForm(instance=album)
            # PESMA
            pesma = pesma_form.save(commit=False)
            pesma.izvodjac = izvodjac
            pesma.album = album
            pesma.dodao = user
            pesma.save()
            
            messages.success(request, f'Pesma sačuvana! Čeka se na odobrenje admina.\n Hvala na pomoći!')
            return redirect('index')

    else:
        izvodjac_form = IzvodjacForm()
        album_form = AlbumForm()
        pesma_form = PesmaForm()

    title = 'Dodaj Akorde'
    
    context = {
        'pesma_form': pesma_form,
        'izvodjac_form': izvodjac_form,
        'album_form': album_form,
        'title': title
    }

    return render(request, 'pesmarica/dodaj_akorde.html', context)



