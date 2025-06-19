from django import forms
from .models import Cotisation, Person
from django.contrib.auth.forms import AuthenticationForm

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
  recherche = forms.CharField(
        label='Recherche',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'code unique...'
        })
    )


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password'].label = "Mot de passe"
 