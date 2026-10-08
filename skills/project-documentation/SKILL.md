---
name: project-documentation
description: Met à jour la documentation complète du projet Angular après des changements de structure, code, algorithmes, conception, standardisation, exemples, schémas ou skills .claude, et produit la documentation technique et fonctionnelle d'un module migré quand module= est fourni. Utiliser quand le développeur demande une mise à jour de documentation projet, un audit de documentation obsolète, la synchronisation de src/app avec src/app/main/pages/code-documentation, la documentation technique/fonctionnelle d'un module, ou la documentation d'un skill .claude spécifique.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# Project Documentation

Met à jour la documentation du projet Angular à partir des changements réellement présents dans le code. Le skill couvre deux usages :

1. **Mode global** — mettre à jour la documentation projet après des changements de structure, code, algorithmes, conception, standardisation, exemples, schémas ou skills.
2. **Mode skill ciblé** — documenter ou mettre à jour la documentation d'un skill `.claude` précis, comme dans l'ancien comportement.

Toujours lire `references/project-documentation-update-contract.md` avant de modifier des fichiers.

## Charger les ressources associées si besoin

- Lire `references/project-documentation-update-contract.md` avant toute mise à jour globale.
- Lire `references/code-documentation-contract.md` et `references/html-patterns.md` avant de modifier la page Angular.
- Utiliser `templates/documentation-technique.template.md` et `templates/documentation-fonctionnelle.template.md` comme structure de départ à l'étape 7 (mode `module=`).
- Consulter `examples/module-documentation-example.md` pour calibrer le niveau de détail attendu sur un module migré.

## Input attendu

```text
update-docs [since=<git-ref>] [scope=<path|all>] [mode=quick|full] [dry-run]
skill=<nom-du-skill> [icon=<material-icon>] [badge=<label-badge>]
```

### Paramètres du mode global

- `update-docs` : déclenche la mise à jour globale de la documentation projet.
- `since=` : référence Git optionnelle pour comparer les changements (`HEAD~1`, `main`, un hash de commit). Si absent, utiliser `git status`, `git diff` et l'analyse structurelle du projet.
- `scope=` : chemin optionnel à analyser (`src/app/main/modules/orderWorkflow`, `src/app/main/pages/code-documentation`, `.claude/skills`, ou `all`). Par défaut : `all`.
- `mode=quick|full` : `quick` met à jour seulement les sections impactées évidentes ; `full` vérifie aussi la cohérence entre code, docs, exemples, schémas et page Angular. Par défaut : `full`.
- `module=` : nom du module migré. Si fourni, produire **en plus** la documentation technique et fonctionnelle de ce module (voir étape 7) avec la mise à jour prévue.
- `dry-run` : produire un rapport des changements à faire sans éditer les fichiers.

### Paramètres du mode skill ciblé

- `skill=` : nom exact du dossier sous `.claude/skills/`.
- `icon=` : icône Material optionnelle.
- `badge=` : badge optionnel (`Automatisation`, `Génération`, `Analyse`, `Qualité`, etc.).

## Fichiers cibles principaux

- Page Angular : `src/app/main/pages/code-documentation/code-documentation.component.ts`
- Contenu HTML : `src/app/main/pages/code-documentation/code-documentation.component.html`
- Styles : `src/app/main/pages/code-documentation/code-documentation.component.scss`
- Docs Markdown : `src/app/main/pages/code-documentation/docs/*.md`
- Exemples : `src/app/main/pages/code-documentation/examples/*`
- Schémas : `src/app/main/pages/code-documentation/schemas/*.json`
- Style contract : `src/app/main/pages/code-documentation/documentation.angular-style.json`
- Skills : `.claude/skills/**`
- Documentation technique du module migré : `src/app/main/pages/code-documentation/docs/modules/<module>/documentation-technique.md`
- Documentation fonctionnelle du module migré : `src/app/main/pages/code-documentation/docs/modules/<module>/documentation-fonctionnelle.md`

## Workflow global recommandé

### 1. Créer l'inventaire des changements

Exécuter l'inventaire depuis la racine du projet :

```bash
python .claude/skills/project-documentation/scripts/project_change_inventory.py --root . --out .claude/tmp/documentation-change-inventory.md
```

Si `since=` est fourni :

```bash
python .claude/skills/project-documentation/scripts/project_change_inventory.py --root . --since <git-ref> --out .claude/tmp/documentation-change-inventory.md
```

Lire ensuite le rapport généré. S'il n'y a pas de dépôt Git, faire une analyse structurelle avec `Glob`, `Grep` et `Read`.

### 2. Classer les changements

Classer chaque changement dans une ou plusieurs catégories :

| Catégorie | Exemples à chercher | Documentation à mettre à jour |
|---|---|---|
| Structure | nouveau module, composant, service, route, dossier | `architecture`, `modules-list`, `README`, docs de démarrage |
| Code API | inputs/outputs, interfaces, types, services, méthodes publiques | sections composants/services, `docs/*.md`, schémas JSON |
| Algorithme | filtres, stats, workflow métier, calcul, mapping payload/API | sections workflow, services, exemples d'utilisation |
| Conception | changement d'architecture, signaux Angular, séparation config/service/composants | `architecture`, `best-practices`, style JSON |
| Standardisation | conventions, naming, hiddenParams, validations, patterns réutilisables | `10-best-practices.md`, exemples, schémas |
| Skill | nouveau skill ou modification `.claude/skills/**` | section skills de la page Angular + docs associées |
| Documentation | docs déjà modifiées | vérifier cohérence nav ↔ HTML ↔ Markdown |

### 3. Comparer documentation existante et code réel

Ne jamais écrire une documentation uniquement depuis le nom des fichiers. Lire les fichiers impactés.

Pour chaque changement important :
- identifier le comportement réel dans le code ;
- vérifier si la page Angular le décrit déjà ;
- vérifier si un fichier `docs/*.md`, `examples/*` ou `schemas/*.json` doit être synchronisé ;
- corriger les sections obsolètes au lieu d'ajouter des doublons ;
- ajouter une nouvelle section seulement si aucune section existante ne correspond.

### 4. Mettre à jour la page Angular `code-documentation`

Lire `references/code-documentation-contract.md` et `references/html-patterns.md`.

Mettre à jour :
1. `navSections` dans le TypeScript si une nouvelle section ou sous-section est ajoutée.
2. Les snippets TypeScript si les exemples affichés changent.
3. Le HTML si le contenu visible change.
4. Le SCSS seulement si des classes nécessaires n'existent pas déjà.

Règles obligatoires :
- les `id` HTML doivent correspondre aux `children` dans `navSections` ;
- les snippets doivent être déclarés avant `scrollToSection()` ;
- les snippets doivent utiliser des backticks ;
- les accolades `{token}` visibles dans le HTML doivent être échappées en `{{ '{' }}token{{ '}' }}` ;
- ne pas inventer de classe CSS sans l'ajouter dans le SCSS.

### 5. Mettre à jour les docs Markdown, exemples et schémas

Utiliser la carte suivante :

| Fichier | Quand le modifier |
|---|---|
| `README.md` | vue d'ensemble, contenu, ordre de lecture, changement majeur de scope |
| `docs/01-getting-started.md` | objectif, structure projet/module, exemple minimal |
| `docs/02-module-configuration.md` | `JsonData`, `ColumnConfig`, `ActionItem`, configuration centrale |
| `docs/03-dynamic-table.md` | table, colonnes, filtres table, tri, outputs |
| `docs/04-dynamic-filters.md` | filtres simples/avancés, valeurs uniques, reset |
| `docs/05-dynamic-forms.md` | génération formulaire, labels, selects, validation, payload |
| `docs/06-actions-buttons.md` | `ACTIONS_API`, `type_action`, confirmation, impression, hiddenParams |
| `docs/07-services-api.md` | endpoints, services, API, interpolation URL/body, erreurs |
| `docs/08-statistics-pivot.md` | statistiques, groupby, pivot table, calculs |
| `docs/09-workflow-cloture.md` | workflow métier, étapes, composants métier |
| `docs/10-best-practices.md` | conventions, standardisation, anti-patterns, règles d'équipe |
| `examples/*` | exemples copiables quand l'API publique change |
| `schemas/*.json` | contrat JSON quand les champs attendus changent |
| `documentation.angular-style.json` | règles de style/documentation quand les conventions changent |

### 6. Mode skill ciblé rétrocompatible

Si l'utilisateur fournit `skill=<nom>`, documenter uniquement ce skill comme l'ancien workflow :
1. lire `.claude/skills/<nom>/SKILL.md` ;
2. lire ses `references/`, `scripts/`, `templates/`, `examples/` si présents ;
3. ajouter ou mettre à jour la section correspondante dans `code-documentation` ;
4. mettre à jour les snippets d'invocation ;
5. vérifier TS/HTML/SCSS.

Pour ce mode, utiliser aussi `references/html-patterns.md`.

### 7. Documentation technique et fonctionnelle du module migré

Quand `module=<module>` est fourni (dernière étape de la chaîne de migration, après validation), produire **deux documents** dédiés au module migré, avec la mise à jour prévue :

1. **Documentation technique** — `docs/modules/<module>/documentation-technique.md`, à partir de `templates/documentation-technique.template.md` :
   - architecture du module (config-driven : `config.service.ts`, composants génériques utilisés, `types.ts`) ;
   - endpoints API consommés (méthodes, payloads, params, erreurs) ;
   - `COLUMNS_API`, `ACTIONS_API`, dropdowns et interpolation URL/body réellement implémentés ;
   - dépendances (services partagés, authentification) et points d'extension.
2. **Documentation fonctionnelle** — `docs/modules/<module>/documentation-fonctionnelle.md`, à partir de `templates/documentation-fonctionnelle.template.md` :
   - objectif métier du module et besoin couvert ;
   - parcours utilisateur, écrans, filtres et actions disponibles ;
   - règles de gestion validées et workflow/transitions de statut ;
   - rôles/profils et messages utilisateur.

Voir `examples/module-documentation-example.md` pour un exemple de niveau de détail attendu.

Sources à croiser pour ces documents :
- le code réel du module (`src/app/main/modules/<module>/**`) ;
- quand ils existent, les livrables de la chaîne : `frontend-rules.md` et `technico-fonctionnel.md` (skill `webforms-rules-doc`) et la spec Swagger utilisée par `swagger-angular-module`.

Ne jamais documenter depuis le seul nom des fichiers : lire le code et refléter la mise à jour réellement présente. Si une section module existe déjà dans la page Angular `code-documentation`, la mettre à jour au lieu de créer un doublon.

### 8. Contrôle final

Toujours lancer les contrôles disponibles :

```bash
npx tsc --noEmit --project tsconfig.app.json 2>&1 | grep -i "code-documentation\|error"
```

Si le projet ne peut pas compiler dans l'environnement courant, exécuter au minimum :

```bash
grep -R "<section id=\|<h2 id=\|<h3 id=" -n src/app/main/pages/code-documentation/code-documentation.component.html
grep -R "id: '" -n src/app/main/pages/code-documentation/code-documentation.component.ts
```

Vérifier aussi :
- aucun doublon d'id HTML ;
- chaque child `navSections` pointe vers un `id` HTML ;
- aucun `{token}` non échappé dans le HTML ajouté ;
- les snippets référencés dans le HTML existent dans le TS ;
- les exemples Markdown/TS restent cohérents avec les types et schémas.

## Format de réponse finale

```text
Résultat :
- Mode                : update-docs / skill ciblé
- Scope analysé       : <all ou chemin>
- Base de comparaison : <git ref / status courant / analyse structurelle>
- Changements trouvés : <résumé par catégories>
- Fichiers mis à jour : <liste>
- Sections Angular    : <ajoutées / modifiées / inchangées>
- Docs Markdown       : <liste>
- Doc technique module : <chemin ou n/a>
- Doc fonctionnelle module : <chemin ou n/a>
- Exemples / schémas  : <liste>
- Compilation         : ok / erreurs détectées / non exécutée + raison
- Avertissements      : <points à valider humainement>
```
