from django.contrib import admin
from .models import Vehicule

# Register your models here.
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
  list_display=('immatriculation', 'type_vehicule', 'disponible', 'capacite_kg', 'entreprise')
  list_editable=('type_vehicule',)
  search_fields=('immatriculation',)
  ordering=('-created_at',)
  list_per_page=10
  date_hierarchy='created_at'
  fieldsets=(
    ("Information general",
    {
      "fields":("immatriculation","disponible",)
    }),
    ("Vehicule Info",
    {
      "fields":("capacite_kg", "type_vehicule", "entreprise",)
    }),
    ("dates",
    {
      "fields":("created_at","updated_at",)
    }),
  )
  readonly_fields=("created_at","updated_at",)
