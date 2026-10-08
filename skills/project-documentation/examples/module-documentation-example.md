# Exemple - documentation d'un module migré (orderWorkflow)

Cet exemple illustre le résultat attendu de l'étape 7 (`module=orderWorkflow`), à utiliser comme repère de niveau de détail. Ce n'est pas un contenu à recopier tel quel dans un nouveau module.

## documentation-technique.md (extrait)

```markdown
## 1. Architecture du module

- Emplacement : `src/app/main/modules/orderWorkflow/`
- Fichiers config-driven : `services/config.service.ts`, `types.ts`
- Composants génériques utilisés : data-table, filter, action-modal, statistic

## 2. Endpoints API consommés

| Endpoint | Méthode | Usage | Payload | Erreurs gérées |
|---|---|---|---|---|
| /api/v1/standard-api/orders | GET | getDataApi | - | 401/403/500 |
| /api/v1/standard-api/orders/{id}/validate | POST | action Valider | { comment } | 400/409 |
```

## documentation-fonctionnelle.md (extrait)

```markdown
## 1. Objectif métier

Permet de clôturer une commande en fin de période, avec validation
hiérarchique avant verrouillage définitif du dossier.

## 4. Workflow / transitions de statut

En cours --(valider)--> En attente validation --(approuver)--> Clôturé
                                              --(rejeter)-----> En cours
```

## Points d'attention observés sur cet exemple

- Ne documenter le workflow de statuts que si les transitions sont réellement implémentées dans le code (méthodes `valider`/`approuver`/`rejeter` trouvées dans le service ou le composant), jamais supposées depuis le nom du module.
- Croiser `frontend-rules.md` (skill `webforms-rules-doc`) pour les libellés de messages utilisateur plutôt que de les inventer.
- Si `technico-fonctionnel.md` existe déjà pour ce module, réutiliser ses règles de gestion validées au lieu de les reformuler différemment.
