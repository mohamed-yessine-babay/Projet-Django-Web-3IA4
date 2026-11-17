from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import OffreForm
from .models import Offre


class OffreListView(ListView):
    model = Offre
    template_name = "offres/liste.html"
    context_object_name = "offres"


class OffreDetailView(DetailView):
    model = Offre
    template_name = "offres/details.html"


class OffreCreateView(CreateView):
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:liste")


class OffreUpdateView(UpdateView):
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:liste")


class OffreDeleteView(DeleteView):
    model = Offre
    template_name = "offres/confirmer_suppression.html"
    success_url = reverse_lazy("offres:liste")
