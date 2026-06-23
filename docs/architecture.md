# Architecture

## Stack

- Django 5
- Django REST Framework + drf-spectacular
- PostgreSQL
- WhiteNoise for static files
- Gunicorn in the container runtime

## Layers

- **accounts**: local authentication, registration, login, roles
- **boards**: projects, boards, columns, labels, project membership, board UI
- **tasks**: task lifecycle, comments, movement, task detail UI
- **core**: audit events and shared base models

## Design choices

- Session auth is used for the browser app because it is simple, secure, and battle-tested.
- The auth backend is isolated so LDAP/AD can be added later by registering another backend.
- Business actions go through service functions to keep audit logging and state transitions consistent.
- REST endpoints are separate from the UI so automation can integrate without scraping HTML.
