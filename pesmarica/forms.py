from django import forms
from .models import Album, Izvodjac, Pesma
from django.db.models import Q
from django.core.exceptions import ValidationError
import re

def validate_chords(text):
    pattern = re.compile(r'(\b[A-G](\d*((maj|m)*#?b?)(add|sus|maj|aug|dim)?)*(\d*))')

    matches = pattern.finditer(text)
    for match in matches:
        if not match:
            return False
        else:
            return True

class IzvodjacForm(forms.ModelForm):
    ime = forms.CharField(label='Izvođač: ', max_length=100)
    class Meta:
        model = Izvodjac
        fields = ['ime']

class AlbumForm(forms.ModelForm):
    naziv_albuma = forms.CharField(label='Album: ', max_length=250)
    class Meta:
        model = Album
        fields = ['naziv_albuma']

class PesmaForm(forms.ModelForm):

    CHOICES = (
        ('Za početnike', 'Za početnike'),
        ('Srednje', 'Srednje'),
        ('Teško', 'Teško')
    )

    naziv_pesme = forms.CharField(label='Naziv pesme: ', max_length=100)

    choices = [('Rok', 'Rok' ), ('Narodno', 'Narodno')]
    zanr = forms.ChoiceField(label='Žanr: ', choices=choices)

    tonalitet = forms.CharField(label='Tonalitet: ', max_length=3)
    takt = forms.CharField(label='Takt: ', initial='4/4', max_length=10)
    tempo = forms.IntegerField(label='Tempo: ')
    ritam = forms.CharField(label='Ritam: ', max_length=30)
    sekcije = forms.CharField(label='Definiši sekcije pesme: ', max_length=50)
    forspil = forms.CharField(label='Akordi za foršpil: ', widget=forms.Textarea(attrs={'class': 'txt-format'}))
    strofa = forms.CharField(label='Akordi za strofu: ', widget=forms.Textarea(attrs={'class': 'txt-format'}))
    predrefren = forms.CharField(label='Akordi za predrefren: ', required=False, widget=forms.Textarea(attrs={'class': 'txt-format'}))
    refren = forms.CharField(label='Akordi za refren: ', widget=forms.Textarea(attrs={'class': 'txt-format'}))
    drugo = forms.CharField(label='Dodatna sekcija: ', help_text='Akordi za solo/improvizaciju itd.', required=False, widget=forms.Textarea(attrs={'class': 'txt-format'}))
    aranzman = forms.CharField(label='Aranžman: ', max_length=100)
    tezina = forms.ChoiceField(
        label='Težina: ',
        help_text='Koliko je teško odsvirati pesmu?',
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=CHOICES,
    )

    def clean_tempo(self):
        tempo = self.cleaned_data.get('tempo')

        if tempo < 60:
            raise forms.ValidationError('Tempo ne može biti manji od 60 BPM')
        else:
            return tempo

    def clean_forspil(self):
        forspil = self.cleaned_data.get('forspil')

        if not validate_chords(forspil):
            raise forms.ValidationError('Da niste zaboravili akorde?')
        else:
            return forspil

    def clean_strofa(self):
        strofa = self.cleaned_data.get('strofa')

        if not validate_chords(strofa):
            raise forms.ValidationError('Da niste zaboravili akorde?')
        else:
            return strofa

    def clean_predrefren(self):
        predrefren = self.cleaned_data.get('predrefren')
        if predrefren:
            if not validate_chords(predrefren):
                raise forms.ValidationError('Da niste zaboravili akorde?')
            else:
                return predrefren
    
    
    def clean_refren(self):
        refren = self.cleaned_data.get('refren')

        if not validate_chords(refren):
            raise forms.ValidationError('Da niste zaboravili akorde?')
        else:
            return refren

        
    def clean_drugo(self):
        drugo = self.cleaned_data.get('drugo')
        if drugo:

            if not validate_chords(drugo):
                raise forms.ValidationError('Da niste zaboravili akorde?')
            else:
                return drugo

    # def clean(self):
    #     form_data = self.cleaned_data
    #     print(form_data)

    #     if Pesma.objects.filter(Q(izvodjac__icontains=form_data['izvodjac']) & Q(naziv_pesme__icontains=form_data['naziv_pesme'])):
    #         raise ValidationError('Akordi za ovu pesmu već postoje.')
    #     return form_data

    class Meta:
        model = Pesma
        fields = ['naziv_pesme', 'zanr', 'tonalitet', 'takt', 'tempo', 'ritam', 'sekcije',
        'forspil', 'strofa', 'predrefren', 'refren', 'drugo', 'aranzman', 'tezina'
        ]