from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import EntrepriseForm, UtilisateurCreationForm, UtilisateurForm
from .models import Entreprise, Utilisateur


class EntrepriseListView(ListView):
    model = Entreprise
    template_name = "entreprises/liste.html"
    context_object_name = "entreprises"


class EntrepriseDetailView(DetailView):
    model = Entreprise
    template_name = "entreprises/details.html"


class EntrepriseCreateView(CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:liste")


class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:liste")


class EntrepriseDeleteView(DeleteView):
    model = Entreprise
    template_name = "entreprises/confirmer_suppression.html"
    success_url = reverse_lazy("entreprises:liste")


class UtilisateurListView(ListView):
    model = Utilisateur
    template_name = "entreprises/utilisateurs_liste.html"
    context_object_name = "utilisateurs"


class UtilisateurDetailView(DetailView):
    model = Utilisateur
    template_name = "entreprises/utilisateur_details.html"


class UtilisateurCreateView(CreateView):
    model = Utilisateur
    form_class = UtilisateurCreationForm
    template_name = "entreprises/utilisateur_form.html"
    success_url = reverse_lazy("entreprises:utilisateur-liste")


class UtilisateurUpdateView(UpdateView):
    model = Utilisateur
    form_class = UtilisateurForm
    template_name = "entreprises/utilisateur_form.html"
    success_url = reverse_lazy("entreprises:utilisateur-liste")


class UtilisateurDeleteView(DeleteView):
    model = Utilisateur
    template_name = "entreprises/utilisateur_confirmer_suppression.html"
    success_url = reverse_lazy("entreprises:utilisateur-liste")
