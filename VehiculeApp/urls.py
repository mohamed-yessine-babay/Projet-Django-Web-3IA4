from django.urls import path

from .views import VehiculeCreateView, VehiculeDeleteView, VehiculeDetailView, VehiculeListView, VehiculeUpdateView

app_name = "vehicules"

urlpatterns = [
    path("", VehiculeListView.as_view(), name="liste"),
    path("ajouter/", VehiculeCreateView.as_view(), name="ajouter"),
    path("<int:pk>/", VehiculeDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", VehiculeUpdateView.as_view(), name="modifier"),
    path("<int:pk>/supprimer/", VehiculeDeleteView.as_view(), name="supprimer"),
]
