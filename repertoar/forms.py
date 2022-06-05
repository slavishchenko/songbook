from django import forms
from pesmarica.models import Pesma
from .models import Repertoar
class RepertoarForm(forms.ModelForm):
    naslov = forms.CharField(label='Naslov: ')
    opis = forms.CharField(label='Opis: ', widget=forms.Textarea(attrs={'rows': '3'}))
    class Meta:
        model = Repertoar
        fields = ['naslov', 'opis', 'javno']

