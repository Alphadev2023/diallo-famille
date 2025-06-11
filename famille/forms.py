from django import forms
from .models import Cotisation

class CotisationForm(forms.ModelForm):
 class Meta:
  model = Cotisation
  fields = ['personne', 'montant', 'mode_paiement', 'reference', 'motif']
  widgets = {
   'mode_paiement': forms.Select(choices=Cotisation.MODE_PAIEMENT_CHOICES),
   'motif': forms.Textarea(attrs={'rows': 2}),
  }
 
 class PaiementForm(forms.Form):
    numero_client = forms.CharField(label="Numéro Orange", max_length=20)
    montant = forms.DecimalField(label="Montant", min_value=100)