from django import forms

from .models import Expedition


class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = (
            "ville_depart",
            "ville_arrive",
            "poids_kg",
            "date_souhaite",
            "description",
            "statut",
            "entreprise",
        )
        widgets = {"date_souhaite": forms.DateInput(attrs={"type": "date"})}
