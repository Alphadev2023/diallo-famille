from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Continent(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


# --------- 2. Pays ---------
class Pays(models.Model):
    nom = models.CharField(max_length=100)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, related_name='pays')

    def __str__(self):
        return self.nom


# --------- 3. Ville ---------
class Ville(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='villes')

    def __str__(self):
        return self.nom


# --------- 4. District ---------
class District(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.nom


# --------- 5. Famille ---------
class Famille(models.Model):
    nom = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='familles')

    def __str__(self):
        return self.nom

class Metier(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank =True)
    metier = models.ForeignKey(Metier, on_delete=models.CASCADE, related_name="personne", null=True, blank=True)
    code_unique = models.CharField(max_length=150, blank=True, null=True, unique=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    genre = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    date_decce = models.DateField(null=True, blank=True)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name='personnes', null=True, blank=True)
    mere = models.ForeignKey('self', null=True, blank=True, related_name='children_from_mother', on_delete=models.SET_NULL)
    pere = models.ForeignKey('self', null=True, blank=True, related_name='children_from_father', on_delete=models.SET_NULL)
    mari = models.ForeignKey("self", null=True, blank=True, related_name="father_from_mother", on_delete=models.SET_NULL)
    reseidence_actuel = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='residence', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Cotisation(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('OM', 'Orange Money'),
        ('CB', 'Carte Bancaire'),
        ('CH', 'Chèque'),
        ('ES', 'Espèces'),
    ]

    personne = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='cotisations')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=2, choices=MODE_PAIEMENT_CHOICES)
    reference = models.CharField(max_length=100, blank=True)
    motif = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.personne} - {self.montant}€ ({self.get_mode_paiement_display()})"

