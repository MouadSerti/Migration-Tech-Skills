---
name: webforms-rules-doc
description: Extract business rules from legacy ASP.NET WebForms and VB.NET source files, then classify every finding on three levels (Backend, Frontend, Technico-fonctionnel) and generate validation-ready documents: backend API rules, frontend interface rules, a technico-functional documentation, and a support validation document. Use when the user provides an IIS application snapshot, a WebForms module folder, or explicit .aspx, .ascx, .master, .vb, .config, .sql, .resx, .asmx, .ashx, or .svc files and asks to document current behavior, validations, workflows, calculations, roles, SQL dependencies, or migration requirements.
argument-hint: "<folder-or-files>"
disable-model-invocation: true
---

# WebForms Rules Documentation

## Goal

Analyze a read-only snapshot of an ASP.NET WebForms / VB.NET module, classify every finding on three levels, and produce the documentation that feeds the downstream migration chain:

1. **Niveau Backend** — `backend-api-rules.md` : règles de gestion à implémenter dans les APIs (consommé par le skill de génération d'API).
2. **Niveau Frontend** — `frontend-rules.md` : règles d'interface, champs, types, validations écran, libellés, dropdowns, actions et comportements UI (consommé par le skill `swagger-angular-module`).
3. **Niveau Technico-fonctionnel** — `technico-fonctionnel.md` : documentation technico-fonctionnelle transverse (parcours, workflow, calculs, dépendances) qui relie le métier au technique, accompagnée de `support-validation.md` pour la validation métier.

Do not modify source files. Only create analysis outputs.

## Inputs

Use `$ARGUMENTS` as the source path list. It may contain:

- one IIS application snapshot folder;
- one WebForms module folder;
- explicit files such as `.aspx`, `.ascx`, `.master`, `.vb`, `.config`, `.sql`, `.resx`, `.asmx`, `.ashx`, `.svc`.

If `$ARGUMENTS` is empty, ask the user for the folder or files to analyze.

## Safety rules

- Never analyze directly in a writable production IIS folder when a snapshot/copy can be used.
- Never run the ASP.NET application or execute application code.
- Treat `.aspx`, `.vb`, `.config`, `.sql`, and `.resx` as source text only.
- Never edit source files from the analyzed application.
- Redact secrets in outputs: connection strings, passwords, tokens, API keys, server names, UNC paths, internal URLs, usernames.
- Mark uncertain findings as `A confirmer`, not as confirmed rules.
- Do not convert script candidates into final business rules without reading the relevant source evidence.

## Workflow

1. Identify the provided source paths from `$ARGUMENTS`.
2. Create an output folder, for example `./outputs/webforms-rules-doc/<module-name>/`.
3. Run the bundled static analyzer:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/analyze_aspx_vb.py" $ARGUMENTS --out-dir "./outputs/webforms-rules-doc" --redact
```

On Windows, if `python` is not available, use:

```powershell
py "${CLAUDE_SKILL_DIR}\scripts\analyze_aspx_vb.py" $ARGUMENTS --out-dir ".\outputs\webforms-rules-doc" --redact
```

4. Read the generated `inventory.md`, `evidence-map.md`, and `analysis.json`.
5. Inspect the most important source files directly, especially:
   - code-behind event handlers such as `Page_Load`, `btn*_Click`, `ddl*_SelectedIndexChanged`, `gv*_RowCommand`;
   - validators and required fields in `.aspx` / `.ascx`;
   - `If`, `ElseIf`, `Select Case`, status/workflow checks;
   - calculations involving amount, TVA, total, remise, solde, plafond, quantity, date rules;
   - role/profile/session checks;
   - SQL calls, stored procedures, tables, and configuration keys.
6. Generate these final files in the output folder, organized on the three levels:
   - **Backend** : `backend-api-rules.md` using `templates/backend-api-rules-template.md`;
   - **Frontend** : `frontend-rules.md` using `templates/frontend-rules-template.md`;
   - **Technico-fonctionnel** : `technico-fonctionnel.md` using `templates/technico-fonctionnel-template.md`, plus `support-validation.md` using `templates/support-validation-template.md` for business validation;
   - `evidence-map.md` with source file and line references;
   - optional `questions-ouvertes.md` if validation questions are many.
7. End with a short summary listing:
   - files created;
   - number of confirmed rules;
   - number of rules to confirm;
   - top blockers before backend implementation.

## Classification rules

Use `references/rule-classification.md` to classify findings.

Required statuses:

- `Confirmee`: supported by clear code evidence and no conflicting interpretation.
- `A confirmer`: probable business behavior but ambiguous, incomplete, or dependent on external SQL/configuration.
- `Technique`: implementation detail, UI plumbing, data access, logging, or infrastructure.
- `Dependance externe`: stored procedure, database table, configuration value, service, report, or external file required to fully understand behavior.

## Output quality requirements

For each business rule, include:

- stable ID, for example `RG-001`;
- rule statement in business language;
- trigger/event;
- conditions;
- expected result;
- source evidence with file and line number;
- validation status;
- backend implementation note when relevant.

Keep `support-validation.md` non-technical and validation-oriented. Keep `backend-api-rules.md` implementation-oriented with API inputs, outputs, errors, dependencies, and suggested endpoint behavior. Keep `frontend-rules.md` interface-oriented (champs, types, validations écran, libellés, dropdowns, actions, comportements UI) so it can directly feed the `swagger-angular-module` generation. Keep `technico-fonctionnel.md` as a transverse technico-functional view linking business behavior to its technical dependencies.

## Supporting files

- `scripts/analyze_aspx_vb.py`: static analyzer that creates inventory and evidence files.
- `templates/support-validation-template.md`: document format for Support & Change validation.
- `templates/backend-api-rules-template.md`: document format for Backend API implementation (niveau Backend).
- `templates/frontend-rules-template.md`: document format for frontend/interface rules consumed by `swagger-angular-module` (niveau Frontend).
- `templates/technico-fonctionnel-template.md`: technico-functional documentation format (niveau Technico-fonctionnel).
- `templates/evidence-map-template.md`: traceability format.
- `references/rule-classification.md`: classification guide.
- `HOW_TO_USE.md`: installation and usage guide for the human user.
- `assets/workflow-usage.png`: visual workflow diagram.
