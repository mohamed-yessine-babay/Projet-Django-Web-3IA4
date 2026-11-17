from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from django.apps import apps
from ExpeditionApp.models import Expedition
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule

# Create your models here.

CAPACITE_INDICATIVE = {
  'camionnette':     {'min': 0,     'max': 1500},
  'fourgon':         {'min': 0,     'max': 3500},
  'camion_porteur':  {'min': 3500,  'max': 19000},
  'semi_remorque':   {'min': 19000, 'max': 26000},
}

class Offre(models.Model):
  date_proposition=models.DateField(auto_now_add=True)
  delai_jours=models.PositiveIntegerField(validators=[MinValueValidator(1, "Le délai doit être >= 1 jour.")], default=1)
  prix=models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(Decimal("0.001"), "un prix nul n'est pas acceptable")])
  statut=models.CharField(max_length=30, choices=[
                                                  ("proposee", "Proposee"),
                                                  ("acceptee", "Acceptee"),
                                                  ("refusee", "Refusee"),
                                                  ("retiree", "Retiree")
                                                  ], default="proposee")
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  expedition=models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='offres')
  vehicule=models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='offres')
  transporteur=models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='offres')

  def __str__(self):
      return f"Offre de {self.transporteur.raison_sociale} sur {self.expedition.reference}"

  def clean(self):
    errors = {}

    if self.transporteur_id and self.transporteur.type_entreprise != "transporteur": # pyright: ignore[reportAttributeAccessIssue]
      errors['transporteur'] = "Seule une entreprise de type 'transporteur' peut faire une offre"

    if self.vehicule_id and self.transporteur_id: # pyright: ignore[reportAttributeAccessIssue]
      if self.vehicule.entreprise_id != self.transporteur_id: # pyright: ignore[reportAttributeAccessIssue]
        errors['vehicule'] = "Le vehicule doit appartenir au transporteur qui propose l'offre"

    if self.pk is None and self.expedition_id and self.expedition.statut != 'publiee': # pyright: ignore[reportAttributeAccessIssue]
      errors['expedition'] = "On ne peut proposer une offre que sur une expedition au statut 'publiee'"

    if self.statut == 'proposee' and self.expedition_id and self.transporteur_id: # pyright: ignore[reportAttributeAccessIssue]
      qs = Offre.objects.filter(
        expedition=self.expedition,
        transporteur=self.transporteur,
        statut='proposee'
      )
      if self.pk:
        qs = qs.exclude(pk=self.pk)
      if qs.exists():
        errors['statut'] = (
          "Ce transporteur a deja une offre au statut 'proposee' sur cette expedition."
        )

    if self.pk is None and self.vehicule_id and not self.vehicule.disponible: # pyright: ignore[reportAttributeAccessIssue]
      errors['vehicule'] = errors.get('vehicule', "") + " Ce vehicule n'est pas disponible."

    if self.vehicule_id and self.expedition_id: # pyright: ignore[reportAttributeAccessIssue]
      type_veh = self.vehicule.type_vehicule
      poids = self.expedition.poids_kg
      limites = CAPACITE_INDICATIVE.get(type_veh)
      if limites:
          if poids < limites['min'] or poids > limites['max']:
              errors['vehicule'] = errors.get('vehicule', "") + (
                  f" Le type '{self.vehicule.get_type_vehicule_display()}' " # pyright: ignore[reportAttributeAccessIssue]
                  f"n'est pas compatible avec un poids de {poids} kg "
                  f"(plage indicative : {limites['min']}–{limites['max']} kg)."
              )

          if self.vehicule.capacite_kg < poids:
            errors['vehicule'] = errors.get('vehicule', "") + (
                f" Capacité réelle du véhicule ({self.vehicule.capacite_kg} kg) insuffisante."
            )

    if errors:
      raise ValidationError(errors)

  def save(self, *args, **kwargs):
    self.full_clean()
    previous_statut = None
    if self.pk:
      previous_statut = Offre.objects.filter(pk=self.pk).values_list('statut', flat=True).first()

    with transaction.atomic():
      is_new_acceptance = (self.statut == 'acceptee' and previous_statut != 'acceptee')
      super().save(*args, **kwargs)
      if is_new_acceptance:
        self._appliquer_cascade_acceptation()

  def _appliquer_cascade_acceptation(self):
    Expedition = apps.get_model("ExpeditionApp", "Expedition")
    Expedition.objects.filter(pk=self.expedition_id).update(statut="attribuee")
    Offre.objects.filter(
      expedition_id=self.expedition_id,
      statut="proposee"
    ).exclude(pk=self.pk).update(statut="refusee", updated_at=timezone.now())
