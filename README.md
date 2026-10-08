# Migration Tech Skills

A collection of [Claude Code](https://claude.com/claude-code) Agent Skills for migrating legacy applications to a modern Angular, config-driven frontend — from documenting legacy business rules, to generating the Angular module from an API contract, to keeping project documentation and test coverage in sync as the migration progresses.

## Skills included

### [`webforms-rules-doc`](skills/webforms-rules-doc)

Analyzes legacy ASP.NET WebForms/VB.NET source (`.aspx`, `.ascx`, `.vb`, `.config`, `.sql`) and extracts business rules into four confidence levels (Confirmed / To confirm / Technical / External dependency). Produces audience-specific markdown deliverables: `backend-api-rules.md`, `frontend-rules.md`, `technico-fonctionnel.md`, `support-validation.md`, plus a file:line traceability `evidence-map.md`. The bundled analyzer script has built-in secret redaction (connection strings, hostnames, UNC paths, tokens) and the skill enforces read-only access to the legacy code — it never modifies or executes it.

This is typically the **first step**: understand what the legacy screen actually does before rebuilding it.

### [`swagger-angular-module`](skills/swagger-angular-module)

Generates, updates, reviews, or deploys an Angular business module from a Swagger/OpenAPI specification, using a config-driven architecture (a single `config.service.ts` drives titles, table columns, actions and dropdowns, on top of a set of shared generic components). Can reconcile the API contract with the `frontend-rules.md` produced by `webforms-rules-doc` for column labels, required fields, and action layout.

```text
module=orders swagger=https://your-api.example.com/openapi.json resource=Order
```

### [`document-claude-skill`](skills/document-claude-skill) / [`project-documentation`](skills/project-documentation)

Keep a project's internal documentation in sync with the actual codebase as the migration progresses: a git-diff-based inventory script classifies recent changes (structure / API / algorithm / convention / skill), then updates the corresponding docs (nav, sections, examples, schemas) with consistency checks. Also generates "technical" and "functional" documentation for a freshly migrated module, cross-referencing the other skills' deliverables.

These two skills are near-identical variants kept from the source project; pick whichever naming convention fits your setup, or merge them.

### [`skillmarket`](skills/skillmarket)

A framework-agnostic test-scenario generator: diffs the current branch against main, classifies changed files (frontend/api/backend/config/test/docs), reads the diffs for impact, and generates Markdown test scenarios plus CSV output consumable by a test-execution pipeline. Works the same whether the target is Angular, React, Vue, or a backend-only change.

## How to use these skills

1. Copy the skill(s) you need into your project's `.claude/skills/` directory:

   ```bash
   cp -r skills/swagger-angular-module /path/to/your-project/.claude/skills/
   ```

2. Open [Claude Code](https://claude.com/claude-code) in your project and invoke the skill, e.g.:

   ```text
   /swagger-angular-module module=orders swagger=./openapi.json
   ```

3. Adapt the `references/` and `templates/` files in each skill to match your own project's module structure, generic components, and API base URL — these skills are written to be adapted, not used as-is against an unrelated codebase.

## Notes

- These skills are intentionally generic and contain no references to any specific company, product, or production system. They were extracted and sanitized from real-world usage in an internal migration project — placeholder URLs, service names, and business domains are used throughout.
- A skill specific to generating backend APIs for one particular ERP/runtime combination, and skills purely about internal test-plan formatting, were intentionally left out of this public repository.
- Contributions of additional migration skills (React, Vue, other legacy stacks) are welcome.

## License

[MIT](LICENSE)
