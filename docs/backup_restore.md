# Backup and restore

## Backup

```bash
docker exec -t <postgres-container> pg_dump -U kanban -d kanban > kanban.sql
```

If you store uploads or other files later, back up those volumes separately.

## Restore

```bash
cat kanban.sql | docker exec -i <postgres-container> psql -U kanban -d kanban
```

After restore, restart the web container if needed.
