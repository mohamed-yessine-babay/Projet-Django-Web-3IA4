from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validateEmail(value):
  if not value:
    raise ValidationError("L'email est obligatoire")
  if not value.endswith("@gmail.com"):
    raise ValidationError("format de l'email est invalide (@gmail.com).")

matricule_validator = RegexValidator(regex=r"^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne]\d{3}$", message="invalide") # type: ignore

# Create your models here.
class Utilisateur(AbstractUser):
  user_id=models.CharField(max_length=10,
                           primary_key=True,
                           editable=False)
  email=models.EmailField(unique=True, validators=[validateEmail])
  telephone=models.CharField(max_length=15,
                             blank=True,
                             null=True)
  role=models.CharField(max_length=15,
                        choices=[('chargeur','Chargeur'),
                                 ('transporteur','Transporteur'),
                                 ('Admin','Administrateur')],
                        default="chargeur")
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  @classmethod
  def _generate_id(cls):
    annee = timezone.now().strftime("%y")  # 2026 avec Y et 26 avec y
    prefixe = f"{annee}user"
    last_element = (cls.objects.filter(user_id__startswith=prefixe).order_by('-user_id').first())
    if last_element:
        try:
            compteur = int(last_element.user_id[-2:]) + 1   # les 2 derniers chiffres
        except (ValueError, IndexError):
            compteur = 0
    else:
        compteur = 0
    if compteur > 99:
        raise ValidationError(f"Limite de 99 utilisateurs atteinte pour l'année {annee}.")
    return f"{prefixe}{compteur:02d}"

  def save(self, *args, **kwargs):
      creation = self._state.adding
      if not self.user_id:
        self.user_id = self._generate_id()
      if creation:
          self.full_clean()
      return super().save(*args, **kwargs)


class Entreprise(models.Model):
  raison_sociale=models.CharField(max_length=100)
  matricule_fiscal=models.CharField(max_length=17, unique=True, validators=[matricule_validator])
  type_entreprise=models.CharField(max_length=15,
                                   choices=[('chargeur','Chargeur'),('transporteur','Transporteur')])
  adress=models.TextField(validators=[MinLengthValidator(20,"L'adresse doit contenir au moins 20 caracteres")])
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  gerant=models.OneToOneField(Utilisateur,
                              on_delete=models.CASCADE,
                              related_name='entreprise')

  def __str__(self):
      return self.raison_sociale

  def save(self, *args, **kwargs):
      self.full_clean()
      super().save(*args, **kwargs)
