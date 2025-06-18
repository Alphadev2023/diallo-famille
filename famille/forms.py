from django import forms
from .models import Cotisation, Person

class PaiementForm(forms.Form):
   numero_client = forms.CharField(label="Numéro Orange", max_length=20)
   montant = forms.DecimalField(label="Montant", min_value=100)

class CotisationForm(forms.ModelForm):
 class Meta:
  model = Cotisation
  fields = ['personne', 'montant', 'mode_paiement', 'reference', 'motif']
  widgets = {
   'mode_paiement': forms.Select(choices=Cotisation.MODE_PAIEMENT_CHOICES),
   'motif': forms.Textarea(attrs={'rows': 2}),
  }
 
 
class SearchPersonByCode(forms.Form):
  code = forms.CharField(
        label='Code personne',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
 