from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Continent, Pays, Ville, District, Person, Cotisation
from .serializers import (
    ContinentSerializer, PaysSerializer, VilleSerializer, DistrictSerializer, PersonneSerializer, CotisationSerializer)
from .forms import SearchPersonByCode 
from .forms import CotisationForm, PaiementForm
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
import json
import random
import uuid
from django.db import models
from django.core.paginator import Paginator
from .models import Cotisation
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

#Custome login with django
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm

def is_gestionnaire(user):
    return user.groups.filter(name='gestionnaire').exists()


@login_required
def index(request):
    form = SearchPersonByCode()
    resultats = []
    
    query = None
    if request.method == 'POST':
        form = SearchPersonByCode(request.POST)
        if form.is_valid():
            query = form.cleaned_data['recherche']
            resultats = Person.objects.filter(
                models.Q(code_unique__icontains=query)
            )
    personne = Person.objects.all()
    paginator = Paginator(personne, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    code_search = Person.objects.filter(pere=query) | Person.objects.filter(mere=query)
    return render(request, 'index.html', {'form': form, 'search': code_search, 'resultats': resultats, 'person': personne, 'page': page})

@login_required
def family_tree(request, code):
    person = get_object_or_404(Person, code_unique=code)
    return render(request, 'family_tree.html', {'person': person})

@login_required
def tree_data(request, code):
    person = get_object_or_404(Person, code_unique=code)

    def build_tree(p):
        return {
            "name": f"{p.nom} {p.prenom}",
            "children": [build_tree(c) for c in set(p.children_from_mother.all()) | set(p.father_from_mother.all())]
        }

    return JsonResponse(build_tree(person))

@login_required
def d3_tree_view(request, code):
    person = get_object_or_404(Person, code_unique=code)
    return render(request, 'tree_d3.html', {'person': person})


@login_required
def ajouter_cotisation(request):
    if request.method == 'POST':
        form = CotisationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cotisation_success')  # À créer ou rediriger ailleurs
    else:
        form = CotisationForm()
    return render(request, 'ajouter_cotisation.html', {'form': form})

### les cotisations 
def cotisation_success(request):
    return HttpResponse("Cotisation enregistrée avec succès !")
### Section de creation d'API pour l'arbre famillial
class ContinentViewSet(viewsets.ModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer

class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

"""class FamilleViewSet(viewsets.ModelViewSet):
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer"""

class PersonneViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonneSerializer

class CotisationViewSet(viewsets.ModelViewSet):
    queryset = Cotisation.objects.all()
    serializer_class = CotisationSerializer


@login_required
def arbre_genealogique(request, code):
    personne = get_object_or_404(Person, code_unique=code)

    # Enfants directs (fils et filles)
    enfants = Person.objects.filter(pere=personne) | Person.objects.filter(mere=personne)

    return render(request, 'arbre_genealogique.html', {
        'personne': personne,
        'enfants': enfants.distinct()
    })



def get_enfants_recursif(personne):
    enfants = Person.objects.filter(pere=personne) | Person.objects.filter(mere=personne)
    enfants = enfants.distinct()

    arbre = []
    for enfant in enfants:
        arbre.append({
            'personne': enfant,
            'enfants': get_enfants_recursif(enfant)
        })
    return arbre

@login_required
def arbre_genealogique_complet(request, code="FMD1"):
    personne = get_object_or_404(Person, code_unique=code)
    arbre = get_enfants_recursif(personne)

    return render(request, 'arbre_genealogique_complet.html', {
        'personne': personne,
        'arbre': arbre
    })

@login_required
def get_arbre_data(personne):
    nodes = []
    edges = []

    def ajouter_noeud_et_enfants(p, parent_id=None):
        cotisations_sum = p.cotisations.aggregate(total=Sum('montant'))['total'] or 0
        label = f"{p.prenom} {p.nom}\nCotisations: {cotisations_sum} XOF"
        nodes.append({'id': p.id, 'label': label})
        if parent_id:
            edges.append({'from': parent_id, 'to': p.id})
        enfants = Person.objects.filter(pere=p) | Person.objects.filter(mere=p)
        enfants = enfants.distinct()
        for enfant in enfants:
            ajouter_noeud_et_enfants(enfant, p.id)

    ajouter_noeud_et_enfants(personne)
    return {'nodes': nodes, 'edges': edges}

@login_required
def arbre_graphique(request, code):
    personne = get_object_or_404(Person, code_unique=code)
    return render(request, 'arbre_graphique.html', {'personne': personne})

@login_required
def arbre_graphique_data(request, code):
    personne = Person.objects.get(code_unique=code)
    data = get_arbre_data(personne)
    return JsonResponse(data)

@login_required
def cotisations_personne(request, code):
    cotisations = Cotisation.objects.filter(code_unique=code).values(
        'id', 'montant', 'date_paiement', 'mode_paiement', 'reference', 'motif'
    ).order_by('-date_paiement')
    return JsonResponse(list(cotisations), safe=False)


@user_passes_test(is_gestionnaire)
@login_required
def api_cotisations(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            personne = Person.objects.get(code_unique=data['personne'])
            montant = float(data['montant'])
            if montant <= 0:
                return JsonResponse({'status': 'error', 'message': 'Montant doit être positif'}, status=400)
            mode_paiement = data['mode_paiement']
            if mode_paiement not in ['Orange Money', 'Espèces', 'Chèque']:
                return JsonResponse({'status': 'error', 'message': 'Mode paiement invalide'}, status=400)
            cotisation = Cotisation.objects.create(
                personne=personne,
                montant=montant,
                mode_paiement=mode_paiement,
                reference=data.get('reference', ''),
                motif=data.get('motif', '')
            )
            return JsonResponse({'status': 'success', 'id': cotisation.id})
        except Person.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Personne inconnue'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Erreur serveur'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
    
def simuler_paiement(request):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero_client']
            montant = form.cleaned_data['montant']
            reference = str(uuid.uuid4())[:8]

            # Simulation de paiement : succès aléatoire
            paiement_reussi = random.choice([True, False])
            statut = 'succès' if paiement_reussi else 'échec'

            Cotisation.objects.create(
                numero_client=numero,
                montant=montant,
                reference=reference,
                statut=statut
            )

            return render(request, 'resultat.html', {
                'reference': reference,
                'statut': statut,
                'montant': montant,
                'numero': numero
            })
    else:
        form = PaiementForm()

    return render(request, 'paiement.html', {'form': form})

