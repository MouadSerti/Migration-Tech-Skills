---
name: swagger-angular-module
description: Generate, update, review, or deploy an Angular business module from Swagger/OpenAPI using config-driven architecture. Use when the developer asks to inspect Swagger endpoints, bodies, params, actions, titles, create a complete module folder, derive the folder name from the API title, copy all existing ts/html files from the reference structure, adapt services/config.service.ts, map TITLE_API/COLUMNS_API/ACTIONS_API/getDataApi/dropdowns, validate the generated module, or prepare deployment.
argument-hint: "module=<name-or-auto> swagger=<path-or-url-or-ui-url> [frontendRules=<path-to-frontend-rules.md>] [title=<api-title>] [resource=<resource>] [template=reference-module-name] [buildCommand=...] [deploy=false|true]"
allowed-tools: Read, Glob, Grep, Bash, Edit, MultiEdit, Write
paths:
  - "src/app/main/modules/**"
  - "src/app/@theme/**"
  - "**/swagger*.json"
  - "**/openapi*.json"
  - "**/*.yaml"
  - "**/*.yml"
  - ".claude/api.sources*.json"
---

# Swagger Angular Module

Use this skill to create or update a config-driven Angular module from Swagger/OpenAPI.

## Expected input

Accept flexible arguments in `$ARGUMENTS`, usually:

```text
module=<target module name> swagger=<swagger/openapi path or URL> [frontendRules=<path to frontend-rules.md>] resource=<business resource>
```

This skill consumes two complementary inputs:

1. **`swagger=`** — the Swagger/OpenAPI spec, used **as it exists** (the contract for endpoints, methods, bodies, params). This is the source of truth for API paths, payload shapes and types.
2. **`frontendRules=`** *(optional)* — the `frontend-rules.md` produced by the `webforms-rules-doc` skill (niveau Frontend). It drives the expected interface: column labels, form fields, required/visibility, screen validations, dropdown sources, action layout and UI behavior, on top of the Swagger contract.

When `frontendRules=` is provided, reconcile both inputs:
- prefer the **frontend rules** for libellés, ordre et visibilité des champs, obligatoire/optionnel, validations écran, libellés et disposition des actions, sources des dropdowns;
- prefer the **Swagger** for endpoint paths, HTTP methods, payload structure and data types;
- if a field exists in the frontend rules but not in the Swagger (or inversely), keep it and flag the gap in the assumptions summary.

If `frontendRules=` is absent, derive the interface from the Swagger alone, as before.

If an input is missing, infer it from the current repository when safe. Ask only when the endpoint/resource mapping is ambiguous.

## Non-negotiable architecture rules

1. Preserve the existing architecture under `src/app/main/modules/[module]/`.
2. For a new module, create a complete folder, not only a standalone `config.service.ts`.
3. If `module=` is missing, derive the folder name from the API title and normalize it to kebab-case without accents.
4. Copy all `.ts` and `.html` files from the reference module structure, including `components/`, `services/`, `app.component.*`, `app.module.ts`, and `types.ts`.
5. Treat `services/config.service.ts` as the main business file that changes after cloning.
6. Do not rewrite generic components unless the Swagger proves the shared contract changed.
7. Keep the app compatible with the existing generic components: `data-table`, `filter`, `form-modal`, `action-modal`, `detail-modal`, `statistic`, `pivot-table`, and `header`.
8. Keep authentication behavior intact: listing/data endpoints that already need token access must remain authenticated.
9. Never hardcode a user-specific identifier if it can be read from application context services.
10. Always summarize assumptions and endpoints used.
11. Never commit, print, or generate tokens/cookies/passwords. Use environment variables for protected Swagger.
12. Never deploy to a remote environment without explicit developer confirmation and an explicit deploy command.

## Load supporting references when needed

- Read `references/module-architecture.md` before changing structure.
- Read `references/folder-generation-and-deploy.md` before creating a new module folder or preparing deployment.
- Read `references/config-service-contract.md` before generating `config.service.ts`.
- Read `references/swagger-mapping-rules.md` before mapping Swagger endpoints to columns/actions.
- Read `references/authenticated-swagger.md` when the Swagger URL is protected, uses Swagger UI Authorize, returns 401/403, or contains `/swagger-ui/`.
- Read `references/quality-checklist.md` before final response.
- Use `templates/config.service.ts.template` when generating a new config file from scratch.
- Use `examples/reference-config-summary.md` to understand the provided reference module example.

## Recommended workflow

1. Inspect the target project structure.
   - Locate `src/app/main/modules/`.
   - Locate a reference module (any existing module in the project).
   - Confirm the reference module contains `app.component.ts`, `app.component.html`, `services/`, `components/`, and `types.ts`.
   - Locate `src/app/@theme/services/user-context.service.ts` and shared services when relevant.
2. Inspect Swagger/OpenAPI.
   - If a local spec is provided, run:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/openapi_summary.py" <swagger-path>
```

   - If a Swagger UI URL is provided, extract the direct spec URL from the `url=` query parameter before fetching.
   - If the direct spec URL is protected by the Swagger UI Authorize flow, read `references/authenticated-swagger.md`, then ask for the auth method only when it is not already configured in `.claude/api.sources*.json`.
   - For protected Swagger endpoints, prefer this local workflow and never store the token in the repository:

```bash
export API_SWAGGER_TOKEN="<token>"
python "${CLAUDE_SKILL_DIR}/scripts/fetch_openapi.py" \
  "https://your-api-server.com/api/swagger/resource-api" \
  --output "/tmp/resource-api.openapi.json" \
  --token-env API_SWAGGER_TOKEN \
  --scheme Bearer
python "${CLAUDE_SKILL_DIR}/scripts/openapi_summary.py" "/tmp/resource-api.openapi.json"
```

   - If no file is provided, search for `swagger.json`, `openapi.json`, `api-docs`, `.yaml`, `.yml`, or `.claude/api.sources*.json`.
3. Identify the API title and target folder name.
   - Prefer `module=` if provided.
   - Otherwise derive the module folder from `title=`, Swagger `info.title`, Swagger tag, or the dominant resource path.
   - Normalize the folder name to kebab-case without accents.
4. Create the full module folder from the reference module before editing business config.
   - Dry-run first when uncertain:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/create_module_from_template.py" \
  --modules-root src/app/main/modules \
  --template reference-module-name \
  --title "<api-title>" \
  --dry-run
```

   - Then create the folder:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/create_module_from_template.py" \
  --modules-root src/app/main/modules \
  --template reference-module-name \
  --module <target-module>
```

5. Identify the resource endpoints.
   - Listing endpoint for `getDataApi()`.
   - Display/detail endpoint.
   - Create endpoint.
   - Update endpoint.
   - Delete endpoint.
   - Dropdown/reference endpoints.
6. Generate or update the copied module's `services/config.service.ts`:
   - `TITLE_API`
   - `COLUMNS_API`
   - `ACTIONS_API`
   - `ConfigService.getDataApi()`
   - dropdown helpers if needed
   - `types.ts` only when the existing contract is insufficient
   - When `frontendRules=` is provided, use `frontend-rules.md` to set column/field labels, required flags, field types, screen validations, dropdown sources and action layout; keep the Swagger as the source of truth for endpoints, methods and payload shapes. Flag any conflict between the two in the assumptions summary.
7. Validate generated config.
   - Run:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_config_service.py" src/app/main/modules/<module>/services/config.service.ts
```

8. Build before deployment.
   - Read `package.json`.
   - Prefer `buildCommand=` from user when provided.
   - Otherwise use `npm run build` if available, or the project's documented command.
9. Prepare deployment.
   - If `deploy=true` and `deployCommand` is provided, show the command and ask for confirmation before running.
   - If no deployment command is provided, do not guess. Return the build result and ask the developer for the deployment command.
10. Return a concise implementation report.

## Mapping rules summary

- `GET list/search/info` usually maps to `getDataApi()`.
- `GET show/detail/{id}` usually maps to an action with `print: true`.
- `POST add/create` maps to an Administration action with `type_action: "modal"`.
- `PUT/PATCH update/modify` maps to a Profil or Administration action with `type_action: "modal"`.
- `DELETE remove/delete/{id}` maps to Administration/Supprimer.
- Path variables in URLs must be available from the selected row or form data.
- Request body fields become action `params` and often become `COLUMNS_API` fields.
- Dropdown fields must use `type: "select"` and either `options`, `localOptions`, or `dropdown.api`.

## Final response format

Always finish with:

```text
Resultat:
- Dossier module cree:
- Fichiers recopies depuis le module modele:
- Fichiers modifies/crees:
- Titre API utilise pour le nommage:
- Endpoints Swagger utilises:
- Fichier frontend-rules utilise (skill 1):
- Champs colonnes generes:
- Actions generees:
- Warnings / hypotheses:
- Commandes de verification/build:
- Statut deploiement:
```
