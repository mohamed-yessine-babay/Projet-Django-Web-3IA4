from django.db import models

# Create your models here.
class Expedition(models.Model):
  reference=models.CharField(max_length=10,
                             unique=True,
                             auto_created=True)
  ville_depart=models.CharField(max_length=15)
  ville_arrive=models.CharField(max_length=15)
  poids_kg=models.DecimalField(max_digits=10, decimal_places=2)
  date_souhaite=models.DateTimeField()
  description=models.TextField()
  statut=models.CharField(max_length=20,
                          choices=[('publiee','Publiee'), ('attribuee','Attribuee'), ('en_cours','En Cours'), ('livree', 'Livree'), ('annulee','Annulee')], default='publiee')
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  entreprise=models.ForeignKey('EntrepriseApp.Entreprise', on_delete= models.CASCADE, related_name='expedition')


  