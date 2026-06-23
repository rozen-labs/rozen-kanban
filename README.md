# Rozen Kanban

Self-hosted, YouTrack-style Kanban for software teams.

## What it ships

- Session-based authentication with local user registration/login
- Role-based access control: Admin, Manager, Developer
- Multiple projects/workspaces
- Kanban boards with configurable columns
- Drag-and-drop task movement
- Assignment, priorities, labels, due dates, comments, and audit trail
- Search and filtering
- Modern responsive UI with dark mode
- PostgreSQL-backed production deployment
- OpenAPI docs and automated tests
- Docker Compose and GHCR delivery

## Quick start

```bash
docker compose up -d --build
```

## Default admin bootstrap

Set these variables before first start:

- `BOOTSTRAP_ADMIN_USERNAME`
- `BOOTSTRAP_ADMIN_EMAIL`
- `BOOTSTRAP_ADMIN_PASSWORD`

The entrypoint runs migrations, creates/updates the admin, and boots the app.

## Docker image

```bash
docker pull ghcr.io/rozen-labs/rozen-kanban:latest
```

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Deployment](docs/deployment.md)
- [Operations](docs/operations.md)
- [Backup and restore](docs/backup_restore.md)
- [Contributing](CONTRIBUTING.md)
