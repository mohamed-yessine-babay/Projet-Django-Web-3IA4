from django.utils import timezone
from django.contrib import admin, messages
from django.db.models import QuerySet
from .models import Expedition

# Register your models here.

class EnRetardFilter(admin.SimpleListFilter):
  title = 'en retard'
  parameter_name = 'en_retard'

  def lookups(self, request, model_admin):
    return [('oui', 'OUI'), ('non', 'NON')]

  def queryset(self, request, queryset):
    today = timezone.now().date()
    if self.value() == 'oui':
      return queryset.filter(statut='publiee', date_souhaite__lt=today)
    if self.value() == 'non':
      return queryset.exclude(statut='publiee', date_souhaite__lt=today)

@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
  list_display=('reference', 'ville_depart', 'ville_arrive', 'poids_kg', 'date_souhaite', 'description', 'statut')
  list_filter=('date_souhaite', EnRetardFilter)
  list_editable=('statut',)
  search_fields=('reference',)
  ordering=('-created_at',)
  list_per_page=10
  date_hierarchy='created_at'
  actions=['make_it_livree']

  fieldsets=(
    ("Information general",
    {
      "fields":("reference", "ville_depart", "ville_arrive", "statut")
    }),
    ("Expedition Info",
    {
      "fields":("poids_kg", "date_souhaite", "description","entreprise")
    }),
    ("dates",
    {
      "fields":("created_at","updated_at")
    }),
  )
  readonly_fields=("reference", "created_at", "updated_at")

  @admin.action(description="Clôturer les expéditions sélectionnées")
  def make_it_livree(self, req, queryset):
    liste = queryset.filter(statut='en_cours')
    liste_ignored = queryset.exclude(statut='en_cours').count()
    errors = []
    nbr_success = 0
    for exp in liste:
      exp.statut = 'livree'
      try:
        exp.save()
        nbr_success += 1
      except Exception as e:
        errors.append(f"{exp.reference} : this expedition had an error")
    if nbr_success:
      self.message_user(
        req,
        f"{nbr_success} expeditions clôturées",
        messages.SUCCESS
      )
    if liste_ignored:
      self.message_user(
        req,
        f"{liste_ignored} expeditions ignorées",
        messages.WARNING
      )
    for e in errors:
      self.message_user(
        req, e, messages.ERROR
      )
