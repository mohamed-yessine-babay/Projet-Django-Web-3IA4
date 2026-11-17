from django.urls import path

from .views import (
    EntrepriseCreateView,
    EntrepriseDeleteView,
    EntrepriseDetailView,
    EntrepriseListView,
    EntrepriseUpdateView,
    UtilisateurCreateView,
    UtilisateurDeleteView,
    UtilisateurDetailView,
    UtilisateurListView,
    UtilisateurUpdateView,
)

app_name = "entreprises"

urlpatterns = [
    path("", EntrepriseListView.as_view(), name="liste"),
    path("ajouter/", EntrepriseCreateView.as_view(), name="ajouter"),
    path("<int:pk>/", EntrepriseDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", EntrepriseUpdateView.as_view(), name="modifier"),
    path("<int:pk>/supprimer/", EntrepriseDeleteView.as_view(), name="supprimer"),
    path("utilisateurs/", UtilisateurListView.as_view(), name="utilisateur-liste"),
    path("utilisateurs/ajouter/", UtilisateurCreateView.as_view(), name="utilisateur-ajouter"),
    path("utilisateurs/<str:pk>/", UtilisateurDetailView.as_view(), name="utilisateur-detail"),
    path("utilisateurs/<str:pk>/modifier/", UtilisateurUpdateView.as_view(), name="utilisateur-modifier"),
    path("utilisateurs/<str:pk>/supprimer/", UtilisateurDeleteView.as_view(), name="utilisateur-supprimer"),
]
