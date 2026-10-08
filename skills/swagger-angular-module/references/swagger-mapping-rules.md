# Regles de mapping Swagger vers module Angular

## Selection des endpoints

Chercher les endpoints par priorite:

1. path contenant le nom de la ressource.
2. tags Swagger egaux ou proches de la ressource.
3. operationId contenant list/info/show/add/update/delete.
4. summary/description contenant les mots metier.

## Roles des endpoints

| Role Angular | Swagger/API probable | Resultat |
|---|---|---|
| Listing | GET list, info, search, all | `getDataApi()` |
| Detail | GET show, detail, findById | action Afficher |
| Creation | POST add, create, save | action Ajouter |
| Modification | PUT/PATCH update, modify | action Modifier |
| Suppression | DELETE delete, remove | action Supprimer |
| Dropdown | GET standard, reference, list small | `dropdown.api` ou helper |

## Extraction champs

1. Lire `requestBody.content.application/json.schema`.
2. Suivre les `$ref` dans `components.schemas`.
3. Extraire `properties` et `required`.
4. Completer avec les champs retournes par le listing si le schema response est plus riche.
5. Ne pas inclure les champs techniques non utiles dans les formulaires: createdAt, updatedAt, audit, token, password, etc., sauf demande explicite.

## Labels

Transformer les noms techniques en libelles lisibles:

- `nom_beneficiaire` -> `Nom Beneficiaire`
- `id_classe` -> `ID Classe`
- `date_de_naissance` -> `Date de Naissance`

Garder les accents en francais quand possible.

## Parametres path

Pour un endpoint `/resource/{id}`:

- verifier si `id` correspond a `id_resource`, `id`, `uuid`, etc.
- si le path utilise `{id}` mais la colonne s'appelle `id_ressource`, garder `api: ".../{id}"` seulement si le composant remplace correctement `{id}`.
- sinon utiliser le nom reel attendu par le composant existant.

## Contexte utilisateur

Si un endpoint a besoin de parametres contextuels comme un identifiant utilisateur, un identifiant de groupe ou une region:

- Les recuperer depuis les services de contexte applicatif au runtime.
- Ne pas les hardcoder dans la configuration du module.
- Les injecter dans `getDataApi()` et les endpoints d'action de maniere dynamique selon la session authentifiee de l'utilisateur.

## Ambiguites a signaler

Toujours signaler:

- plusieurs endpoints candidats pour listing.
- body manquant pour POST/PUT.
- params Swagger sans colonne correspondante.
- colonnes select sans source d'options.
- changement necessaire dans `types.ts`.
