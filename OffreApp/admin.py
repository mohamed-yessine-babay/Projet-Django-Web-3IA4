from django.contrib import admin
from django.utils.html import format_html

from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
  ordering=("-created_at",)
  list_per_page=10
  date_hierarchy="created_at"
  list_filter=("expedition", "transporteur", "statut",)
  list_display=("expedition", "transporteur", "prix", "statut_colore")
  autocomplete_fields = ()

  readonly_fields=(
      "statut_colore",
      "date_proposition",
      "created_at",
      "updated_at",
  )

  fieldsets=(
      (
          "Détails de l'offre",
          {
              "fields":(
                  "expedition",
                  "transporteur",
                  "vehicule",
              )
          },
      ),
      (
          "Conditions",
          {
              "fields":(
                  "prix",
                  "delai_jours",
              )
          },
      ),
      (
          "Suivi",
          {
              "fields":(
                  "statut_colore",
                  "statut",
                  "date_proposition",
              )
          },
      ),
      (
          "dates",
          {
              "fields":("created_at","updated_at",)
          },
      ),
  )

  @admin.display(description="Statut")
  def statut_colore(self, obj):
    couleurs = {
        "proposee": "#F0AD4E",
        "acceptee": "#5CB85C",
        "refusee": "#D9534F",
        "retiree": "#777777",
    }

    return format_html(
        (
            '<span style="color:white;background:{};'
            'padding:3px 8px;border-radius:4px;">'
            '{}</span>'
        ),
        couleurs.get(obj.statut, "#999"),
        obj.get_statut_display(),
    )
