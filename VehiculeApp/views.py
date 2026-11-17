from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import VehiculeForm
from .models import Vehicule


class VehiculeListView(ListView):
    model = Vehicule
    template_name = "vehicules/liste.html"
    context_object_name = "vehicules"


class VehiculeDetailView(DetailView):
    model = Vehicule
    template_name = "vehicules/details.html"


class VehiculeCreateView(CreateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    success_url = reverse_lazy("vehicules:liste")


class VehiculeUpdateView(UpdateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    success_url = reverse_lazy("vehicules:liste")


class VehiculeDeleteView(DeleteView):
    model = Vehicule
    template_name = "vehicules/confirmer_suppression.html"
    success_url = reverse_lazy("vehicules:liste")
