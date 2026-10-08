# Creation du dossier module et deploiement

## Objectif

Pour un nouveau module, produire un dossier complet dans `src/app/main/modules/<nom-module>/`, pas seulement un `config.service.ts` isole.

Le nom du dossier doit etre adapte au titre de l'API quand l'utilisateur ne donne pas explicitement `module=`.

## Regle de nommage du dossier

Ordre de priorite pour choisir le nom du dossier:

1. `module=<nom>` fourni par l'utilisateur.
2. Titre explicite fourni par l'utilisateur, par exemple `titre="Gestion des receptions"`.
3. `info.title` du Swagger/OpenAPI.
4. `tags[0].name` ou nom de ressource le plus frequent dans les paths.
5. Dernier recours: demander au developpeur.

Normaliser le nom en kebab-case sans accents:

```text
Gestion des commandes -> gestion-des-commandes
Reception API -> resource-api
Orders/Invoices -> orders-invoices
```

Ne jamais creer un dossier avec espaces, accents, slash, apostrophe ou majuscules.

## Creation du dossier complet

Pour un nouveau module, copier la structure complete du module de reference avant de modifier la configuration metier.

Structure attendue apres generation:

```text
src/app/main/modules/<nom-module>/
├── app.component.ts
├── app.component.html
├── app.module.ts
├── types.ts
├── services/
│   ├── config.service.ts
│   ├── app.service.ts
│   └── pivot-table.service.ts
└── components/
    ├── action-modal.component.ts
    ├── data-table.component.ts
    ├── detail-modal.component.ts
    ├── filter.component.ts
    ├── form-modal.component.ts
    ├── header.component.ts
    ├── pivot-table.component.ts
    └── statistic.component.ts
```

Copier les fichiers `.ts`, `.html`, `.scss`, `.css` et `.json` du module modele. Dans la structure actuelle, les composants generiques sont volontairement dupliques dans le dossier module. Les recopier pour que le nouveau module soit autonome et conforme a l'existant.

Commande recommandee:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/create_module_from_template.py" \
  --modules-root src/app/main/modules \
  --template reference-module-name \
  --title "<titre-api>"
```

Ou si le nom de module est deja connu:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/create_module_from_template.py" \
  --modules-root src/app/main/modules \
  --template reference-module-name \
  --module reception
```

Utiliser `--dry-run` avant l'ecriture quand le mapping est incertain. Utiliser `--force` uniquement si le developpeur a demande d'ecraser un module existant.

## Fichiers a modifier apres copie

Apres la copie, adapter principalement:

1. `services/config.service.ts`
   - `TITLE_API` avec le titre API/metier.
   - `COLUMNS_API` avec les champs de listing, body et schemas.
   - `ACTIONS_API` avec les actions detectees dans Swagger.
   - `getDataApi()` avec le bon endpoint de listing.
   - dropdowns/options si le Swagger expose des endpoints de reference.
2. `types.ts` seulement si le contrat generique ne couvre pas les champs necessaires.
3. Les composants `.ts` et `.html` seulement si une preuve montre que le composant partage/generique ne supporte pas le besoin.

## Fichiers a ne pas changer sans raison forte

- `app.component.ts`
- `app.component.html`
- `services/app.service.ts`
- `services/pivot-table.service.ts`
- `components/*.component.ts`

Ces fichiers doivent etre recopies comme dans le module modele pour garder la meme structure UI et les memes composants partages.

## Verification avant deploiement

Apres generation:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_config_service.py" src/app/main/modules/<nom-module>/services/config.service.ts
npm run build
```

Si le projet utilise une autre commande, lire `package.json` et utiliser la commande existante, par exemple `npm run build:prod` ou `ng build`.

## Deploiement

Ne jamais deployer automatiquement vers un environnement distant sans confirmation explicite du developpeur.

Workflow autorise:

1. Generer le dossier module.
2. Valider `config.service.ts`.
3. Executer le build local.
4. Si le developpeur a donne une commande de deploiement claire, l'afficher puis demander confirmation avant execution.
5. Si aucune commande n'est fournie, terminer avec les commandes de verification et la commande de deploiement a lancer manuellement.

Exemples de parametres acceptes:

```text
deploy=false
deployCommand="npm run deploy:dev"
buildCommand="npm run build"
```

Par defaut: `deploy=false`.
