# Contrat config.service.ts

## Exports obligatoires

```ts
export const TITLE_API = [{ title: "..." }];
export const COLUMNS_API = [/* ColumnConfig[] */];
export const ACTIONS_API = [/* ActionCategory[] */];
```

## TITLE_API

Format:

```ts
export const TITLE_API = [{
  title: "gestion des [ressource]"
}];
```

## COLUMNS_API

Chaque colonne doit respecter ce minimum:

```ts
{
  field: "nom_champ",
  label: "Libelle lisible",
  type: "text" | "number" | "date" | "select" | "boolean",
  filterable: true,
  validators: { required: true },
  statistics: [],
  defaultStatistics: []
}
```

### Choix du type

- `integer`, `number`, `long`, `double`, `float` -> `number`
- `date`, `date-time`, champ contenant `date_` -> `date`
- `boolean` -> `boolean`
- enum, statut, categorie, genre, type, region, annee -> souvent `select`
- sinon -> `text`

### Validators recommandes

- required: selon Swagger `required` ou champ critique.
- min/max: pour number si Swagger contient minimum/maximum.
- minLength/maxLength: pour string si Swagger contient minLength/maxLength.
- pattern: si Swagger contient pattern.

## ACTIONS_API

Format:

```ts
export const ACTIONS_API = [
  {
    category: "Profil",
    items: [
      {
        title: "Modifier",
        api: "https://.../{id}",
        method: "PUT",
        params: ["id", "nom", "..."],
        type_action: "modal",
        print: false
      }
    ]
  }
];
```

## Categories recommandees

- `Profil [ressource]`: afficher et modifier l'element selectionne.
- `Administration`: ajouter et supprimer.
- `Documents` ou `Impression`: actions de print/export si present.

## Parametres d'action

- Les `params` doivent correspondre a des champs connus dans `COLUMNS_API`, au selected item, ou a des valeurs contextuelles.
- Pour `POST`, utiliser les champs du request body.
- Pour `PUT/PATCH`, utiliser l'id + champs modifiables du body.
- Pour `DELETE`, utiliser l'id necessaire dans le path.
- Pour `GET detail/show`, utiliser les champs affichables et `print: true` si l'action sert a imprimer/afficher.

## ConfigService

`ConfigService` doit garder:

- base URL.
- helpers d'identite/context:
  - `getProviderUserLoger()` si Swagger a besoin de provider/user.
  - `getIdGroupe()` ou equivalent si le module depend du groupe.
- `getDataApi()` qui construit l'URL de listing.
- gestion dropdown si colonnes `select`.

## Dropdowns

Une colonne select peut utiliser:

```ts
{ type: "select", options: [...] }
```

ou:

```ts
{ type: "select", localOptions: "id_groupe" }
```

ou:

```ts
{ type: "select", dropdown: { api: "sections", params: { ... } } }
```

Ajouter un nouveau nom dans `StandardDropdownApi` si necessaire.
