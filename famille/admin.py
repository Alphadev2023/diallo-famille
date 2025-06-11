from django.contrib import admin
from .models import (
    Continent, Pays, Ville, District,
    Famille, Person, Cotisation
)

# Register your models here.

@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
 list_display = ['nom']


@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
 list_display = ['nom', 'continent']
 list_filter = ['continent']


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
 list_display = ['nom', 'pays']
 list_filter = ['pays']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
 list_display = ['nom', 'ville']
 list_filter = ['ville']


@admin.register(Famille)
class FamilleAdmin(admin.ModelAdmin):
 list_display = ['nom', 'district']
 list_filter = ['district']
 search_fields = ['nom', 'prenom']


class MariFilter(admin.ModelAdmin):
 class Media:
  js = ('/media/js/person_admin.js',)
 

  
 
 

admin.site.register(Person, MariFilter)
