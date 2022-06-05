from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from pesmarica.models import Pesma
from repertoar.models import Repertoar
from repertoar.forms import RepertoarForm
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import random

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.success(request, f'Uspešno se napravili nalog! Možete se prijaviti.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Zbirka Pesama | Registracija'
    }

    return render(request, 'users/register.html', context)

@login_required
def profile(request):

    sve_pesme = list(Pesma.objects.all().filter(odobrio_admin=True).exclude(dodao_id=request.user.id))
    try:
        nasumicno = random.sample(sve_pesme, 5)
    except:
        nasumicno = random.sample(sve_pesme, len(sve_pesme))

    form = RepertoarForm()

    user_id = request.user.id
    repertoari = Repertoar.objects.filter(autor=user_id).order_by('datum_dodavanja').reverse()
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            if 'cancel' in request.POST:
                return redirect('profile')
            elif 'delete' in request.POST:
                user = User.objects.filter(username__icontains=u_form.cleaned_data['username'])
                if user is not None:
                    user.delete()
                    messages.success(request, f'Uspešno se obrisali nalog!')
                    return redirect('index')
            else:
                u_form.save()
                p_form.save() 
                messages.success(request, f'Sačuvano!')
                return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()

    context = {
        'title': f'Zbirka Pesama | Profil',
        'u_form': u_form,
        'p_form': p_form,
        'nasumicno': nasumicno,
        'form': form,
        'repertoari': repertoari,
    }
    return render(request, 'users/profile.html', context)

@login_required
def moje_pesme(request):
    user_id = request.user.id
    moje_pesme = Pesma.objects.filter(dodao=user_id)
    title = f'Zbirka Pesama | Profil'
    #* Nasumicne pesme
    sve_pesme = list(Pesma.objects.all().filter(odobrio_admin=True).exclude(dodao_id=request.user.id))
    try:
        nasumicno = random.sample(sve_pesme, 5)
    except:
        nasumicno = random.sample(sve_pesme, len(sve_pesme))

    form = RepertoarForm()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            if 'cancel' in request.POST:
                return redirect('profile')
            elif 'delete' in request.POST:
                user = User.objects.filter(username__icontains=u_form.cleaned_data['username'])
                if user is not None:
                    user.delete()
                    messages.success(request, f'Uspešno se obrisali nalog!')
                    return redirect('index')
            else:
                u_form.save()
                p_form.save() 
                messages.success(request, f'Sačuvano!')
                return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()
    

    context = {
        'title': title,
        'u_form': u_form,
        'p_form': p_form,
        'moje_pesme': moje_pesme,
        'nasumicno': nasumicno,
        'form': form,
    }

    return render(request, 'users/moje-pesme.html', context)

        