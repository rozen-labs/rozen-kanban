# Deployment

## Requirements

- Docker and Docker Compose
- A PostgreSQL-backed persistent volume

## Single-command deployment

```bash
make up
```

Or, if you want the raw command:

```bash
DOCKER_CONFIG=$HOME/.docker sudo -E docker compose up -d --build
```

## Environment variables

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `BOOTSTRAP_ADMIN_USERNAME`
- `BOOTSTRAP_ADMIN_EMAIL`
- `BOOTSTRAP_ADMIN_PASSWORD`

## First boot

The container entrypoint applies migrations, optionally bootstraps the admin account, collects static assets, then starts Gunicorn.
