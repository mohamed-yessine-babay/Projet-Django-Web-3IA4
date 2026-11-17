# AI_LOG.md

## Entrée 1 — 2026-10-05

- **Outil IA utilisé :** ChatGPT
- **Prompt :** "Génère le modèle Django Offre pour TransConnect selon le cahier des charges fourni (section III du PDF)."
- **Sortie obtenue (résumé) :** Modèle Offre avec `prix` en CharField, `delai_jours` en IntegerField, `date_proposition` en auto_now=True, et une méthode save() vide.
- **Écarts identifiés vs cahier des charges :**
  1. `prix` en `CharField` au lieu de `DecimalField`
  2. `delai_jours` en `IntegerField` au lieu de `PositiveIntegerField`
  3. `date_proposition` avec `auto_now=True` au lieu de `auto_now_add=True`
  4. Méthode `save()` redondante (appel inutile à super())
- **Correction apportée et justification :**
  1. `DecimalField(max_digits=10, decimal_places=2)` — un prix est une valeur monétaire, pas une chaîne.
  2. `PositiveIntegerField` — un délai en jours ne peut pas être négatif (contrainte du cahier des charges).
  3. `auto_now_add=True` — timestamp figé à la création, non modifié à chaque save.
  4. Suppression de la méthode `save()` — aucune logique ajoutée par rapport au parent.