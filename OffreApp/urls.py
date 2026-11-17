from django.urls import path

from .views import OffreCreateView, OffreDeleteView, OffreDetailView, OffreListView, OffreUpdateView

app_name = "offres"

urlpatterns = [
    path("", OffreListView.as_view(), name="liste"),
    path("ajouter/", OffreCreateView.as_view(), name="ajouter"),
    path("<int:pk>/", OffreDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", OffreUpdateView.as_view(), name="modifier"),
    path("<int:pk>/supprimer/", OffreDeleteView.as_view(), name="supprimer"),
]
