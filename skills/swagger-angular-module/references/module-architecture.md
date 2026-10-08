# Architecture Module Angular Config-Driven

## Structure cible

```text
src/app/main/modules/[module]/
├── app.component.ts
├── app.component.html
├── app.module.ts
├── types.ts
├── services/
│   ├── config.service.ts
│   ├── app.service.ts
│   └── pivot-table.service.ts
└── components/
    ├── data-table.component.ts
    ├── filter.component.ts
    ├── form-modal.component.ts
    ├── action-modal.component.ts
    ├── detail-modal.component.ts
    ├── statistic.component.ts
    ├── pivot-table.component.ts
    └── header.component.ts
```

## Responsabilites

- `config.service.ts`: configuration metier du module. C'est le fichier principal a generer.
- `app.service.ts`: assemble titre, colonnes, actions et data. Ne le modifier que si le contrat de config change.
- `types.ts`: types partages du module. Modifier seulement si nouveau type necessaire.
- `components/*`: composants generiques. Ne pas les personnaliser par module sauf preuve claire.

## Regles de modification

1. Pour un nouveau module, copier la structure du module de reference puis adapter `config.service.ts`.
2. Garder les noms de constantes attendus par `app.service.ts`:
   - `TITLE_API`
   - `COLUMNS_API`
   - `ACTIONS_API`
3. Garder `ConfigService.getDataApi()` comme source de l'URL data.
4. Garder `UserContextService` pour recuperer les identifiants utilisateur/contextuels.
5. Ne pas casser les imports relatifs `../types` et `./config.service`.

## Anti-patterns

- Ne pas dupliquer la logique generique dans chaque module.
- Ne pas mettre les endpoints dans les composants.
- Ne pas utiliser de valeurs fixes comme id utilisateur, id groupe, provider user si un service les fournit.
- Ne pas remplacer les composants generiques par des composants specifiques sans demande explicite.


## Regle importante: dossier complet par titre/API

Pour un nouveau module, le resultat attendu est un dossier complet sous `src/app/main/modules/<nom-module>/`.

Le `<nom-module>` peut etre donne par l'utilisateur ou derive du titre de l'API. Toujours normaliser ce nom en kebab-case sans accents.

Le workflow correct est:

```text
Swagger/API title
  -> nom de dossier normalise
  -> copie complete de la structure du module de reference
  -> adaptation de services/config.service.ts
  -> verification build
  -> preparation deploiement
```

Ne pas generer uniquement un fichier `config.service.ts` hors dossier. Le developpeur doit obtenir un module Angular complet avec les memes fichiers `.ts` et `.html` que la structure existante.
