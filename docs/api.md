# API

Base path: `/api/`

## Documentation

- OpenAPI schema: `/api/schema/`
- Swagger UI: `/api/docs/`

## Endpoints

- `GET /api/projects/`
- `POST /api/projects/`
- `GET /api/tasks/`
- `GET /api/tasks/{id}/`
- `PATCH /api/tasks/{id}/update_fields/`
- `POST /api/tasks/{id}/move/`
- `GET|POST /api/tasks/{id}/comments/`

## Auth

Session authentication is enabled by default. For API automation, use a logged-in session or add JWT later without changing the domain model.
