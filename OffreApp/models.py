from django.db import models

# Create your models here.
class Offre(models.Model):
  date_proposition=models.DateTimeField(auto_created=True)
  deal_jours=models.PositiveIntegerField()
  prix=models.DecimalField(max_digits=10, decimal_places=2)
  expedition=models.ForeignKey('ExpeditionApp.Expedition',on_delete=models.CASCADE,related_name='offres')
  vehicule=models.ForeignKey('VehiculeApp.Vehicule',on_delete=models.CASCADE,related_name='offres')
  transporteur=models.ForeignKey('EntrepriseApp.Entreprise',on_delete=models.CASCADE, related_name='offres')