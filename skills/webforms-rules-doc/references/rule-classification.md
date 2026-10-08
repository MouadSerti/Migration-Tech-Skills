# Classification des règles WebForms

## Confirmee

Utiliser ce statut lorsqu'une règle est directement observable dans le code et que son intention métier est claire.

Exemples :

- Un champ est obligatoire via `RequiredFieldValidator` ou `Page.IsValid`.
- Un bouton déclenche une validation avant sauvegarde.
- Un statut passe de `Brouillon` à `Valide` sous une condition explicite.
- Un calcul de total, TVA, remise ou solde est visible dans une expression claire.

## A confirmer

Utiliser ce statut lorsqu'une règle semble métier mais demande une validation humaine.

Exemples :

- La condition dépend d'une procédure stockée non fournie.
- Le sens d'un statut n'est pas clair.
- Une valeur magique apparaît dans le code, par exemple `If type = 3 Then`.
- Le comportement dépend d'une configuration ou d'une session non documentée.

## Technique

Utiliser ce statut pour les éléments qui ne doivent pas être validés comme règles métier.

Exemples :

- Binding GridView.
- Gestion de paging.
- Logging.
- Try/Catch générique.
- Ouverture de connexion SQL.
- Affectation purement visuelle sans conséquence métier.

## Dependance externe

Utiliser ce statut lorsqu'une règle ou un comportement dépend d'un élément externe.

Exemples :

- Procédure stockée.
- Table ou vue SQL.
- `web.config` / `appSettings`.
- `Session(...)`.
- Service externe.
- Fichier réseau.
- Rapport Crystal/RDLC.

## Bonnes pratiques de formulation

Ecrire les règles au format :

> Lorsque `<déclencheur>`, si `<condition>`, alors `<résultat métier>`.

Exemple :

> Lorsque l'utilisateur clique sur Valider, si le montant total est supérieur au plafond autorisé, alors la demande est rejetée et un message d'erreur est affiché.

Eviter :

> Le bouton appelle `SaveData()`.

Préférer :

> Lorsque l'utilisateur enregistre le formulaire, les champs obligatoires sont validés avant la sauvegarde de la demande.
