# Documentation fonctionnelle — {{NomModule}}

> Généré par le skill `document-claude-skill` (étape 7, mode `module=`). Croiser avec `frontend-rules.md` et `technico-fonctionnel.md` (skill `webforms-rules-doc`) quand ils existent. Remplacer chaque `{{placeholder}}` par le contenu réel validé métier.

## 1. Objectif métier

Décrire en 2-3 phrases le besoin couvert par le module et le contexte métier (ex. gestion d'un dossier, workflow de validation, suivi d'un statut).

## 2. Parcours utilisateur

- Écran(s) principal/principaux : {{liste}}
- Filtres disponibles : {{liste}}
- Actions disponibles à l'utilisateur : {{liste}}
- Navigation (accès depuis quel menu, retour vers quel écran) : {{description}}

## 3. Règles de gestion validées

| Règle | Description | Condition d'activation |
|---|---|---|
| {{règle}} | {{description}} | {{statut/rôle/condition}} |

## 4. Workflow / transitions de statut

Décrire les statuts possibles et les transitions autorisées :

```text
{{Statut A}} --({{action}})--> {{Statut B}}
```

- Qui peut déclencher chaque transition : {{rôle/profil}}
- Que se passe-t-il en cas d'erreur ou de refus : {{comportement}}

## 5. Rôles / profils et messages utilisateur

| Rôle/Profil | Actions autorisées | Restrictions |
|---|---|---|
| {{rôle}} | {{actions}} | {{restrictions}} |

| Situation | Message utilisateur affiché |
|---|---|
| {{succès/erreur/confirmation}} | {{texte exact affiché}} |
