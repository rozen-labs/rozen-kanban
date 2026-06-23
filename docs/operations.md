# Operations

## Health and runtime

- The app runs behind Gunicorn.
- Static assets are served by WhiteNoise.
- PostgreSQL holds persistent data.

## Common tasks

- `python manage.py migrate`
- `python manage.py createsuperuser` or the bootstrap command
- `python manage.py bootstrap_admin --username ... --email ... --password ...`

## Logs

Container stdout/stderr are the primary runtime logs.
