# Example Reference Module - Key Points

The reference module provided serves as a pattern for new modules.

## Observed Structure

- Components are generic and reusable.
- `app.service.ts` assembles `TITLE_API`, `COLUMNS_API`, `ACTIONS_API` and fetches data via `ConfigService.getDataApi()`.
- `config.service.ts` contains the business logic: columns, actions, endpoints, dropdowns and user context.

## Main Constants

- `TITLE_API`: title displayed by the module.
- `COLUMNS_API`: table configuration, filters, validations, statistics.
- `ACTIONS_API`: actions by category, with endpoint, method, params, modal/print behavior.

## Patterns to Keep

- `baseUrl = 'https://your-api-server.com/api/v1'` (configure based on your API).
- `standardApiUrl = baseUrl + '/resource-endpoint'`.
- `getContextUser()` retrieves user information from application context services.
- `getDataApi()` constructs the listing endpoint URL.
- `loadDropdownsForColumns()` populates select column options from API dropdowns.

## Important Notes

When creating new modules, do not blindly copy fields from the reference module. Regenerate columns and actions from the Swagger/OpenAPI specification to match your API contract.
