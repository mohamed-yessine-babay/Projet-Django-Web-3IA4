from django.urls import path
import django.contrib.auth.urls

from .views import (
    ExpeditionCreateView,
    ExpeditionDeleteView,
    ExpeditionDetailView,
    ExpeditionListView,
    ExpeditionUpdateView,
    detail_expedition,
)

app_name = "expeditions"

urlpatterns = [
    
    path("", ExpeditionListView.as_view(), name="liste"),
    path("ajouter/", ExpeditionCreateView.as_view(), name="ajouter"),
    path("<int:pk>/", ExpeditionDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", ExpeditionUpdateView.as_view(), name="modifier"),
    path("<int:pk>/supprimer/", ExpeditionDeleteView.as_view(), name="supprimer"),
    path("reference/<str:id>/", detail_expedition, name="detail-reference"),
]
