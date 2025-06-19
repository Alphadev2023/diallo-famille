from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import (
    ContinentViewSet, PaysViewSet, VilleViewSet, DistrictViewSet, PersonneViewSet, CotisationViewSet)


router = DefaultRouter()
router.register(r'continents', ContinentViewSet)
router.register(r'pays', PaysViewSet)
router.register(r'villes', VilleViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'personnes', PersonneViewSet)
router.register(r'cotisations', CotisationViewSet)

urlpatterns = [
 path('', views.index, name='index'),
 path('famille/<str:code>/', views.family_tree, name='family_tree'),
 path('famille/<str:code>/json/', views.tree_data, name='tree_data'),
 path('famille/<str:code>/d3/', views.d3_tree_view, name='d3_tree_view'),
 path('cotisation/ajouter/', views.ajouter_cotisation, name='ajouter_cotisation'),
 path('api/', include(router.urls)),
 path('payer/', views.simuler_paiement, name='simuler_paiement'),
 
 path("login/", views.CustomLoginView.as_view(), name="login"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('cotisation/success/', views.cotisation_success, name='cotisation_success'),
    path('arbre/<str:code>/', views.arbre_genealogique, name='arbre_genealogique'),
     path('arbre/complet/<str:code>/', views.arbre_genealogique_complet, name='arbre_genealogique_complet'),
     path('arbre/graphique/<str:code>/', views.arbre_graphique, name='arbre_graphique'),
    path('arbre/graphique/data/<str:code>/', views.arbre_graphique_data, name='arbre_graphique_data'),
    path('api/cotisations/<str:code>/', views.cotisations_personne, name='cotisations_personne'),
]