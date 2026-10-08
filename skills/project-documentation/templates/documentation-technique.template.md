# Documentation technique — {{NomModule}}

> Généré par le skill `project-documentation` (étape 7, mode `module=`). Remplacer chaque `{{placeholder}}` par le contenu réel observé dans le code du module. Ne jamais laisser un placeholder non résolu dans le document final.

## 1. Architecture du module

- Emplacement : `src/app/main/modules/{{nomModule}}/`
- Fichiers config-driven : `services/config.service.ts`, `types.ts`
- Composants génériques utilisés : {{data-table | filter | form-modal | action-modal | detail-modal | statistic | pivot-table | header}}
- Composants métier spécifiques (le cas échéant) : {{liste}}

## 2. Endpoints API consommés

| Endpoint | Méthode | Usage | Payload | Erreurs gérées |
|---|---|---|---|---|
| {{/rest/...}} | {{GET/POST/PUT/DELETE}} | {{getDataApi / detail / create / update / delete / dropdown}} | {{champs}} | {{codes HTTP gérés}} |

## 3. Configuration `config.service.ts`

### COLUMNS_API

| Champ | Type | Obligatoire | Source |
|---|---|---|---|
| {{champ}} | {{type}} | {{oui/non}} | {{endpoint/dropdown}} |

### ACTIONS_API

| Action | `type_action` | Profil/rôle | Endpoint appelé | `hiddenParams` |
|---|---|---|---|---|
| {{action}} | {{modal/print/confirm}} | {{Administration/Profil/...}} | {{endpoint}} | {{params}} |

### Dropdowns

| Champ | Source (`options` / `localOptions` / `dropdown.api`) | Endpoint (si applicable) |
|---|---|---|
| {{champ}} | {{source}} | {{endpoint}} |

### Interpolation URL/body

Décrire les variables interpolées depuis la ligne sélectionnée ou le formulaire (ex. `{id}` dans l'URL, champs injectés dans le body).

## 4. Dépendances

- Services partagés utilisés : {{ex. UserDetailsService}}
- Authentification : {{comportement observé — token requis sur quels endpoints}}
- Autres modules/services couplés : {{liste}}

## 5. Points d'extension

- Ce qui peut être étendu sans casser le contrat existant : {{ex. ajout de colonnes, nouvelle action}}
- Ce qui ne doit pas être modifié sans revalidation : {{ex. contrat COLUMNS_API partagé avec un autre écran}}
