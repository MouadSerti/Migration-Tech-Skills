# Comment fonctionne le skill `document-claude-skill`

## Évolution du skill

Au départ, ce skill documentait uniquement un skill `.claude` dans la page Angular `code-documentation`. Il a été étendu pour devenir un outil de mise à jour de documentation projet.

Désormais, quand on l'appelle pour mettre à jour la documentation, il analyse les changements dans tout le projet : structure, code, algorithmes, conception, standardisation, exemples, schémas et skills.

## Deux modes d'utilisation

### 1. Mise à jour globale

```text
/document-claude-skill update-docs
/document-claude-skill update-docs since=HEAD~1
/document-claude-skill update-docs scope=src/app/main/modules/orderWorkflow mode=full
/document-claude-skill update-docs dry-run
```

Le skill :
1. génère un inventaire des changements ;
2. classe les impacts documentaires ;
3. lit les fichiers code réellement concernés ;
4. met à jour les fichiers `code-documentation` pertinents ;
5. vérifie la cohérence TypeScript, HTML, Markdown, exemples et schémas ;
6. retourne un rapport final.

### 2. Documentation d'un skill ciblé

```text
/document-claude-skill skill=swagger-angular-module
/document-claude-skill skill=mon-skill icon=build badge=Génération
```

Ce mode conserve l'ancien comportement : lire `.claude/skills/<nom>/`, extraire son workflow, ses références et scripts, puis créer ou mettre à jour sa documentation dans la page Angular.

## Documentation cible

Le skill connaît la structure suivante :

```text
src/app/main/pages/code-documentation/
├── code-documentation.component.ts
├── code-documentation.component.html
├── code-documentation.component.scss
├── README.md
├── docs/
├── examples/
├── schemas/
└── documentation.angular-style.json
```

Il ne modifie pas tout systématiquement. Il choisit les fichiers selon l'impact :
- changement d'architecture → page Angular + README + `01-getting-started.md` ;
- changement d'interface/type → section composant/service + schéma JSON ;
- changement d'algorithme → workflow + exemple ;
- changement de convention → `10-best-practices.md` + `documentation.angular-style.json` ;
- changement de skill → section skills + snippets d'invocation.

## Script d'inventaire

Le script inclus `scripts/project_change_inventory.py` aide Claude Code à démarrer l'analyse.

Il collecte :
- `git status --short` ;
- `git diff --name-status` ;
- `git diff --stat` ;
- une classification documentaire des fichiers ;
- une arborescence utile si Git n'est pas disponible.

Le script ne remplace pas l'analyse du code. Il sert à prioriser les fichiers à lire.

## Règles critiques conservées

- Les IDs `navSections` doivent correspondre aux IDs HTML.
- Les snippets copiables doivent être déclarés dans le TypeScript avant `scrollToSection()`.
- Les accolades visibles dans le HTML doivent être échappées pour éviter `NG5002`.
- Les exemples Markdown, snippets Angular et schémas JSON doivent rester cohérents.
- Toute incertitude doit être signalée dans le rapport final.
