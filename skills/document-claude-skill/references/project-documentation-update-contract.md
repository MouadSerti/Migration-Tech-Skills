# Contrat de mise à jour de documentation projet

Ce contrat définit comment synchroniser la documentation `code-documentation` avec le code réel du projet Angular.

## Objectif

La documentation doit expliquer l'état courant du projet, pas seulement les changements récents. Lorsqu'un changement est détecté, mettre à jour la section existante la plus proche avant d'ajouter une nouvelle section.

## Sources à analyser

| Source | Rôle |
|---|---|
| `src/app/**` | code Angular réel : composants, services, routes, types, styles |
| `src/app/main/modules/**` | modules métier et architecture dynamique |
| `src/app/main/pages/code-documentation/**` | documentation visuelle, markdown, exemples, schémas |
| `.claude/skills/**` | skills automatisant le développement, génération, audit, documentation |
| `package.json`, `angular.json`, `tsconfig*.json` | dépendances, configuration Angular/TypeScript |
| `*.md` racine | README ou notes projet |

## Artefacts de documentation

```text
src/app/main/pages/code-documentation/
├── code-documentation.component.ts      # navigation, snippets, données de doc
├── code-documentation.component.html    # contenu visuel affiché
├── code-documentation.component.scss    # classes utilisées par la doc
├── README.md                            # guide de lecture rapide
├── docs/                                # documentation détaillée Markdown
├── examples/                            # exemples copiables maintenus avec le code
├── schemas/                             # contrats JSON de configuration
└── documentation.angular-style.json     # conventions de style documentaire
```

## Décision de mise à jour

### Modifier une section existante quand

- le composant/service/type est déjà documenté ;
- seule une méthode, input, output, option ou règle change ;
- un exemple devient obsolète ;
- une convention est clarifiée.

### Ajouter une section quand

- un nouveau module ou composant majeur apparaît ;
- un nouveau workflow métier apparaît ;
- un nouveau skill `.claude` devient important pour l'équipe ;
- une nouvelle famille de conventions mérite sa propre ancre de navigation.

### Ne pas documenter quand

- changement purement cosmétique sans impact développeur ;
- renommage interne non visible dans l'API ou les conventions ;
- code expérimental non relié au workflow du projet ;
- détail redondant déjà couvert par un exemple plus clair.

## Dimensions d'analyse obligatoires

### 1. Structure

Chercher : nouveaux dossiers, composants, services, routes, modules, fichiers de type, assets ou skills.

Mettre à jour :
- `architecture` dans la page Angular ;
- `modules-list` si un module métier est ajouté/modifié ;
- `README.md` et `docs/01-getting-started.md` si le parcours de lecture change.

### 2. Code et API publique

Chercher : `@Input`, `@Output`, `input.required`, `output`, interfaces exportées, services injectables, méthodes publiques, routes, providers.

Mettre à jour :
- tableaux Inputs/Outputs dans le TS si utilisés par le HTML ;
- sections HTML des composants ;
- `docs/*.md` associés ;
- `schemas/*.json` si le contrat JSON change.

### 3. Algorithmes et workflows

Chercher : calculs, filtres, statistiques, pivot, mapping payload, interpolation URL/body, étapes métier, signaux/computed/effects.

Mettre à jour :
- sections workflow ;
- exemples copiables ;
- bonnes pratiques si une nouvelle règle d'implémentation est nécessaire.

### 4. Conception

Chercher : changement d'architecture, responsabilité déplacée entre composant/service/config, nouvelle convention de séparation, nouveau pattern Angular.

Mettre à jour :
- `architecture` ;
- `docs/10-best-practices.md` ;
- `documentation.angular-style.json` si la règle doit être réutilisée.

### 5. Standardisation

Chercher : conventions de naming, types de colonnes/actions, hiddenParams, validations, conventions d'URL, gestion d'erreurs.

Mettre à jour :
- `docs/10-best-practices.md` ;
- `examples/*` ;
- `schemas/*.json`.

### 6. Skills

Chercher : nouveaux dossiers `.claude/skills/<nom>`, changements de `SKILL.md`, nouveaux scripts/références.

Mettre à jour :
- section `claude-skill` si elle regroupe les skills ;
- ou nouvelle section dédiée si le skill mérite une documentation autonome ;
- snippets d'invocation dans le TS.

## Ordre de travail recommandé

1. Lire l'inventaire des changements.
2. Ouvrir les fichiers code impactés.
3. Ouvrir les sections de documentation correspondantes.
4. Déterminer : modifier, ajouter, supprimer, ou laisser inchangé.
5. Mettre à jour Markdown/exemples/schémas avant la page Angular si les deux sont concernés.
6. Mettre à jour TS puis HTML puis SCSS.
7. Lancer les contrôles.
8. Produire le rapport final.

## Règles de qualité

- La documentation doit rester utile pour un développeur qui crée ou modifie un module.
- Les exemples doivent compiler conceptuellement avec les interfaces documentées.
- Éviter les longues explications génériques : privilégier le comportement exact du projet.
- Ne pas dupliquer un même exemple dans plusieurs sections sauf nécessité pédagogique.
- Ne pas supprimer une documentation sans vérifier qu'elle est réellement obsolète.
- Signaler les incertitudes dans le rapport final au lieu d'inventer.
