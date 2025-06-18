from rest_framework import serializers
from .models import Continent, Pays, Ville, District, Person, Cotisation

class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ['id', 'nom']


class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['id', 'nom', 'continent']


class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = ['id', 'nom', 'pays']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'nom', 'ville']


"""class FamilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Famille
        fields = ['id', 'nom', 'district']"""


class PersonneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id', 'nom', 'prenom', 'genre', "email","telephone",
           "image", 'date_naissance',
            'famille', 'pere', 'mere'
        ]


class CotisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotisation
        fields = [
            'id', 'personne', 'montant', 'date_paiement',
            'mode_paiement', 'reference', 'motif'
        ]