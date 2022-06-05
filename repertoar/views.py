from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import Repertoar
from .forms import RepertoarForm
from pesmarica.models import Pesma
import random

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


@login_required
def repertoar(request):
    #* Nasumicne pesme
    sve_pesme = list(Pesma.objects.all().filter(odobrio_admin=True).exclude(dodao_id=request.user.id))
    try:
        nasumicno = random.sample(sve_pesme, 5)
    except:
        nasumicno = random.sample(sve_pesme, len(sve_pesme))

    if request.method == 'POST':
    
        form = RepertoarForm(request.POST)
        user = request.user
        if form.is_valid():
            naslov = form.cleaned_data['naslov']                
            repertoar = form.save(commit=False)
            repertoar.autor = user
            repertoar.save()

            # REPERTOAR ID
            repertoar_obj = Repertoar.objects.filter(Q(naslov__icontains=naslov) | Q(autor=user))
            for r in repertoar_obj:
                repertoar_id = r.id

            messages.success(request, f'Repertoar sačuvan!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        form = RepertoarForm()

    user_id = request.user.id
    moji_repertoari = Repertoar.objects.filter(autor_id = user_id).order_by('datum_dodavanja').reverse()[:5]
    repertoari = Repertoar.objects.filter(javno=True).order_by('datum_dodavanja').reverse()
    title = 'Zbirka Pesama | Repertoar'
    
    context = {
        'form': form,
        'title': title,
        'moji_repertoari': moji_repertoari,
        'repertoari': repertoari,
        'nasumicno': nasumicno
    }

    return render(request, 'repertoar/repertoar.html', context)

@login_required
def repertoar_detail(request, pk, slug):

    slug = slug.split('-')
    slug = ' '.join(slug)
    slug = slug.title()

    if request.method == 'GET':
        if Repertoar.objects.filter(naslov__icontains=slug).filter(javno=False):
            for rep in Repertoar.objects.filter(naslov__icontains=slug).filter(javno=False):
                if request.user != rep.autor and not request.user.is_superuser:
                    raise PermissionDenied 
        else:
            pass

    repertoar = Repertoar.objects.filter(naslov__icontains=slug)
    for r in repertoar:
        pesme = r.set.all()

    najnoviji = Repertoar.objects.filter(javno=True).order_by('datum_dodavanja').reverse()[:10]

    title = f'Zbirka pesama | {slug}'

    context = {
        'title': title,
        'repertoar': repertoar,
        'pesme': pesme,
        'najnoviji': najnoviji,
        'slug': slug,
    }
    return render(request, 'repertoar/repertoar_detail.html', context)

class RepertoarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Repertoar
    fields = ['naslov', 'opis', 'javno']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        repertoar = self.get_object()
        if self.request.user == repertoar.autor:
            return True
        return False

class RepertoarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Repertoar

    success_url = '/repertoar'

    def test_func(self):
        repertoar = self.get_object()
        if self.request.user == repertoar.autor:
            return True
        return False

@login_required
def ukloni_pesmu(request, pk, slug, id):
    if request.method == 'POST':
        repertoar = Repertoar.objects.filter(id=pk)
        for polje in repertoar:
            polje.set.remove(id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('index')
    

def dodaj_pesmu(request, id):
    if request.method == 'POST':
        r_name = request.POST['repertoar']
        repertoar = Repertoar.objects.filter(naslov__icontains=r_name)
        for polje in repertoar:
            polje.set.add(id)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('index')
