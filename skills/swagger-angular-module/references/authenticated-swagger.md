# Authenticated Swagger / OpenAPI

Use this reference when the Swagger/OpenAPI source requires the Swagger UI **Authorize** button, a Bearer token, an API key, a cookie, or another protected header.

## Important rule

Do not ask the developer to paste private credentials into generated files. Do not commit tokens, cookies, or passwords. Prefer environment variables or a local temporary downloaded spec.

## Swagger UI URL vs direct spec URL

The developer may provide a Swagger UI URL such as:

```text
https://your-api-server.com/toolstatic/lib/swagger-ui/index.html?url=https://your-api-server.com/api/swagger/resource-api
```

The direct OpenAPI/Swagger spec URL is the `url=` value:

```text
https://your-api-server.com/api/swagger/resource-api
```

Use the direct spec URL when running scripts. If the URL returns HTML, it is the wrong URL or authorization failed.

## Recommended local workflow

1. The developer obtains a valid access token from their normal authenticated environment.
2. The developer exports it locally:

```bash
export API_SWAGGER_TOKEN="paste-token-here"
```

3. Download the protected spec to a temporary local file:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/fetch_openapi.py" \
  "https://your-api-server.com/api/swagger/resource-api" \
  --output "/tmp/resource-api.openapi.json" \
  --token-env API_SWAGGER_TOKEN \
  --scheme Bearer
```

4. Analyze the downloaded file:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/openapi_summary.py" "/tmp/resource-api.openapi.json"
```

5. Generate or update the Angular module using `/tmp/resource-api.openapi.json` as the Swagger input.

## Alternative auth patterns

Bearer token:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/fetch_openapi.py" URL -o /tmp/api.json --token-env API_SWAGGER_TOKEN --scheme Bearer
```

Raw Authorization header:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/fetch_openapi.py" URL -o /tmp/api.json --token-env API_AUTH_HEADER --scheme ""
```

API key header:

```bash
export API_KEY="secret"
python "${CLAUDE_SKILL_DIR}/scripts/fetch_openapi.py" URL -o /tmp/api.json --header-env X-API-Key=API_KEY
```

Cookie-based auth:

```bash
export API_COOKIE="SESSION=..."
python "${CLAUDE_SKILL_DIR}/scripts/fetch_openapi.py" URL -o /tmp/api.json --header-env Cookie=API_COOKIE
```

## Claude Cowork limitation

Claude Cowork usually cannot read the developer's local machine or browser session. For protected Swagger, use one of these inputs:

- upload the downloaded OpenAPI JSON/YAML file;
- provide a secure internal URL accessible to Claude Cowork;
- paste only a sanitized subset of the endpoints, without tokens.

Do not paste production tokens into Claude Cowork unless company policy explicitly allows it.

## What to verify after download

- The downloaded file is JSON or YAML, not HTML.
- The file contains `openapi`, `swagger`, `paths`, or `components`/`definitions`.
- The target resource endpoints exist, for example reception-related list/create/update/delete endpoints.
- Security schemes should be mapped as runtime authentication in the Angular API calls, not as hardcoded values inside `config.service.ts`.
