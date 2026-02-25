# HTTP API Design Guidelines

Rule ID: API-REST-001  
Scope: http-apis

- Use standard HTTP methods according to their semantics:
  - `GET` for safe, idempotent retrieval.
  - `POST` for creation or non-idempotent operations.
  - `PUT` for full updates.
  - `PATCH` for partial updates.
  - `DELETE` for deletion.

Rule ID: API-REST-002  
Scope: http-apis

- Use clear, resource-oriented URIs (e.g. `/users/{id}/orders`) instead of action verbs.
- Avoid encoding operations in query parameters when they should be expressed as resources.

Rule ID: API-REST-003  
Scope: http-apis

- Use consistent response envelopes and error formats across endpoints.
- Always include enough information for clients to understand and remediate errors (e.g. machine-readable `code`, human-readable `message`).

Rule ID: API-REST-004  
Scope: http-apis

- Validate all incoming request data and return appropriate HTTP status codes for invalid input (e.g. `400 Bad Request`, `422 Unprocessable Entity`).
- Do not rely solely on client-side validation.

