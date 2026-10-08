# Backend - Spécification des règles pour APIs

## 1. Contexte

- Module legacy : `<module>`
- Ecran WebForms source : `<aspx / ascx>`
- Code-behind : `<vb>`
- Document Support associé : `support-validation.md`

## 2. Objectif backend

Implémenter dans les APIs les règles de gestion validées depuis le module WebForms legacy, en séparant clairement les règles métier des détails UI ou techniques.

## 3. Règles métier à implémenter

| ID règle | Description métier | Entrées API nécessaires | Sortie attendue | Erreurs / exceptions | Priorité | Source |
|---|---|---|---|---|---|---|
| RG-001 | | | | | | |

## 4. Endpoints suggérés

| Méthode | Endpoint suggéré | Description | Règles appliquées |
|---|---|---|---|
| POST | `/api/<resource>/<action>` | | RG-001 |

## 5. Validations backend

| Champ / donnée | Règle de validation | Code erreur suggéré | Message fonctionnel | Source |
|---|---|---|---|---|
| | | | | |

## 6. Workflow / transitions de statut

| Etat actuel | Action | Condition | Nouvel état | Règle source |
|---|---|---|---|---|
| | | | | |

## 7. Calculs

| ID règle | Formule / logique | Données d'entrée | Précision / arrondi | Source |
|---|---|---|---|---|
| | | | | |

## 8. Dépendances techniques détectées

### Tables / vues SQL

| Nom | Usage probable | Source |
|---|---|---|
| | | |

### Procédures stockées

| Procédure | Usage probable | Paramètres détectés | Source |
|---|---|---|---|
| | | | |

### Sessions / configuration

| Clé | Type | Usage probable | Source |
|---|---|---|---|
| | | | |

## 9. Points bloquants avant implémentation

| ID | Point à clarifier | Equipe responsable | Impact |
|---|---|---|---|
| PB-001 | | Support / Backend / DBA | |

## 10. Checklist backend

- [ ] Toutes les règles `Confirmee` sont mappées à une logique API.
- [ ] Les règles `A confirmer` ne sont pas implémentées sans validation métier.
- [ ] Les dépendances SQL sont confirmées avec DBA ou équipe legacy.
- [ ] Les messages d'erreur fonctionnels sont validés.
- [ ] Les tests unitaires couvrent les validations et calculs.
- [ ] Les tests d'intégration couvrent les transitions de statut.
