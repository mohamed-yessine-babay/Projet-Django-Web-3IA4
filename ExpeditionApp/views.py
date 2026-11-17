from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ExpeditionForm
from .models import Expedition


def liste_expeditions(request):
    expeditions = (
        Expedition.objects
        .filter(statut="publiee")
        .select_related("entreprise")
        .order_by("-created_at")
    )
    return render(request, "expeditions/liste.html", {"liste": expeditions})


def detail_expedition(request, id):
    expedition = get_object_or_404(Expedition, reference=id)
    offres = expedition.offres.select_related("transporteur", "vehicule").order_by("-date_proposition")
    return render(request, "expeditions/details.html", {"expedition": expedition, "offres": offres})


class ExpeditionListView(ListView):
    model = Expedition
    template_name = "expeditions/liste.html"
    context_object_name = "liste"


class ExpeditionDetailView(DetailView):
    model = Expedition
    template_name = "expeditions/details.html"


class ExpeditionCreateView(CreateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    success_url = reverse_lazy("expeditions:liste")


class ExpeditionUpdateView(UpdateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    success_url = reverse_lazy("expeditions:liste")


class ExpeditionDeleteView(DeleteView):
    model = Expedition
    template_name = "expeditions/confirmer_suppression.html"
    success_url = reverse_lazy("expeditions:liste")
