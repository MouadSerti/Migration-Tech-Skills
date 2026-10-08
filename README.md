# Migration Tech Skills

A collection of [Claude Code](https://claude.com/claude-code) Agent Skills for migrating legacy applications and APIs to a modern Angular, config-driven frontend architecture.

These skills teach Claude a repeatable workflow: read a Swagger/OpenAPI contract, map it to a config-driven Angular module (columns, actions, dropdowns, endpoints), and generate a complete, ready-to-review module folder that follows your project's existing conventions.

## Skills included

### [`swagger-angular-module`](skills/swagger-angular-module)

Generate, update, review, or deploy an Angular business module from a Swagger/OpenAPI specification, using a config-driven architecture (a single `config.service.ts` drives titles, table columns, actions and dropdowns, on top of a set of shared generic components).

Typical use:

```text
module=orders swagger=https://your-api.example.com/openapi.json resource=Order
```

What it does:

- Inspects the Swagger/OpenAPI contract for endpoints, request/response schemas and parameters.
- Optionally reconciles it with a `frontend-rules.md` document describing expected UI behavior (labels, required fields, dropdown sources, action layout).
- Clones a reference module's folder structure so the new module stays consistent with the rest of the codebase.
- Generates `config.service.ts` (`TITLE_API`, `COLUMNS_API`, `ACTIONS_API`, `getDataApi()`, dropdown helpers).
- Validates the generated config and (optionally) runs the project's build before proposing deployment.
- Never commits or hardcodes tokens/credentials — protected Swagger sources are fetched via environment variables (see `references/authenticated-swagger.md`).

See [`skills/swagger-angular-module/SKILL.md`](skills/swagger-angular-module/SKILL.md) for the full workflow, architecture rules and supporting references.

## How to use these skills

1. Copy the skill folder you need into your project's `.claude/skills/` directory:

   ```bash
   cp -r skills/swagger-angular-module /path/to/your-project/.claude/skills/
   ```

2. Open [Claude Code](https://claude.com/claude-code) in your project and invoke the skill, e.g.:

   ```text
   /swagger-angular-module module=orders swagger=./openapi.json
   ```

3. Adapt `references/module-architecture.md` and `templates/config.service.ts.template` to match your own project's module structure, generic components and API base URL — this skill is written to be adapted, not used as-is against an unrelated codebase.

## Notes

- These skills are intentionally generic and contain no references to any specific company, product, or production system. They were extracted and sanitized from real-world usage in an internal project — placeholder URLs, service names, and business domains are used throughout.
- Contributions of additional migration skills (React, Vue, other legacy stacks) are welcome.

## License

[MIT](LICENSE)
