from django.db import models
from EntrepriseApp.models import Entreprise
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Expedition(models.Model):
  reference=models.CharField(max_length=20,
                             unique=True,
                             editable=False)
  ville_depart=models.CharField(max_length=100)
  ville_arrive=models.CharField(max_length=100)
  poids_kg=models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0.001, "Un poids nul ne peux pas etre accepte")])
  date_souhaite=models.DateField()
  description=models.TextField(max_length=100)
  statut=models.CharField(max_length=20,
                          choices=[('publiee','Publiee'), ('attribuee','Attribuee'), ('en_cours','En Cours'), ('livree', 'Livree'), ('annulee','Annulee')], default='publiee')
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  entreprise=models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='expedition')

  def __str__(self):
      return self.reference

  def clean(self):
    super().clean()
    if self.entreprise_id and self.entreprise.type_entreprise != "chargeur": # type: ignore
      raise ValidationError({"entreprise": "Seule une entreprise de type 'chargeur' peut publier une expédition."})

  def save(self, *args, **kwargs):
    self.full_clean()
    if not self.reference:
      self.reference = self._generate_ref()
    return super().save(*args, **kwargs)

  @classmethod
  def _generate_ref(cls):
    annee = timezone.now().strftime("%y")  # 2026 avec Y et 26 avec y
    prefixe = f"EXP-{annee}-"
    last_element = (cls.objects.filter(reference__startswith=prefixe).order_by('-reference').first())
    compteur = int(last_element.reference[-5:]) + 1 if last_element else 1
    if compteur > 99999:
      raise ValueError(f"limite de 99999 pour annee {annee}")
    return f"{prefixe}{compteur:05d}"
