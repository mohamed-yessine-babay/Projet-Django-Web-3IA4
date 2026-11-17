from django import forms

from .models import Offre


class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = (
            "delai_jours",
            "prix",
            "statut",
            "expedition",
            "vehicule",
            "transporteur",
        )
