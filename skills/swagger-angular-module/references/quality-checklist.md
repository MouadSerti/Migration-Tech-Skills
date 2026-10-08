# Checklist qualite avant livraison

## Verification structure

- [ ] Le module cible existe ou a ete cree sous `src/app/main/modules/[module]`.
- [ ] `config.service.ts` exporte `TITLE_API`, `COLUMNS_API`, `ACTIONS_API`.
- [ ] `ConfigService` contient `getDataApi()`.
- [ ] Les imports TypeScript restent valides.

## Verification Swagger

- [ ] Chaque endpoint utilise est liste dans le rapport final.
- [ ] Le listing vient d'un endpoint GET coherent.
- [ ] Les actions POST/PUT/DELETE utilisent les bons methods HTTP.
- [ ] Les path params sont presents dans la ligne selectionnee, le formulaire ou le contexte.

## Verification colonnes

- [ ] Chaque colonne a `field`, `label`, `type`, `filterable`, `statistics`, `defaultStatistics`.
- [ ] Les champs obligatoires Swagger ont un validator `required`.
- [ ] Les types Swagger sont convertis en types Angular compatibles.
- [ ] Les selects ont `options`, `localOptions` ou `dropdown`.

## Verification actions

- [ ] Chaque `action.params` correspond a une colonne ou un champ contextuel.
- [ ] `POST` n'inclut pas d'id auto-genere sauf si l'API le demande.
- [ ] `PUT/PATCH` inclut l'id requis + champs modifiables.
- [ ] `DELETE` n'envoie que le minimum necessaire.
- [ ] Les actions d'affichage ont `print: true` si elles sont utilisees pour imprimer/afficher.

## Verification securite

- [ ] Aucun token n'est hardcode.
- [ ] Aucun id utilisateur/groupe n'est hardcode.
- [ ] Les endpoints authentifies gardent le comportement existant.
- [ ] Les URLs sensibles ou environnements doivent etre confirmes si passage dev/prod.

## Rapport final

Inclure:

- fichiers modifies/crees.
- endpoints utilises.
- champs generes.
- actions generees.
- warnings/hypotheses.
- commandes pour verifier.
