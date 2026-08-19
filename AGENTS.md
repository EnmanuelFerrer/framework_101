# Odoo 19 Estate Module - Development Context

## Project Overview

Dockerized Odoo 19 development environment for learning the Server Framework 101 tutorial. Contains a single custom addon (`estate`) for real estate property management.

**Author:** Enmanuel Ferrer

## Project Structure

```
framework_101/
├── addons/estate/           # Custom addon (mounted at /mnt/custom-addons in Docker)
│   ├── __manifest__.py      # Module manifest (v19.0.1.0.0)
│   ├── __init__.py          # Root package init
│   ├── models/
│   │   ├── __init__.py
│   │   └── property.py      # Main property model
│   ├── views/
│   │   ├── estate_property_views.xml   # Tree + Form views
│   │   └── estate_menus.xml            # Menu hierarchy
│   ├── security/
│   │   └── ir.model.access.csv         # CRUD permissions
│   └── data/
│       └── res.country.state.csv       # Country states
├── config/odoo.conf         # Primary Odoo config (used by Docker)
├── docker-compose.yml       # Odoo + PostgreSQL services
├── odoo.Dockerfile          # Odoo 19 image with ruff
├── postgres.Dockerfile      # PostgreSQL 17 + pgvector
├── ruff.toml                # Python linter config
├── .pylintrc                # Pylint + pylint-odoo
├── .isort.cfg               # Import sorter config
└── pyrightconfig.json       # Type checker config
```

## Architecture

- **Odoo 19** running in Docker (port from `.env`, default 8069)
- **PostgreSQL 17** with pgvector extension
- Custom addons mounted from `addons/` to `/mnt/custom-addons`
- Config loaded from `config/odoo.conf` (mounted to `/etc/odoo`)

## Commands

### Start environment
```bash
docker compose up -d
```

### Stop environment
```bash
docker compose down
```

### Restart Odoo (after code changes)
```bash
docker compose restart odoo
```

### Update module (after model/view changes)
```bash
docker compose exec odoo odoo -d <db_name> -u estate --stop-after-init
```

### Access Odoo shell
```bash
docker compose exec odoo odoo shell -d <db_name>
```

### Run ruff linter
```bash
ruff check addons/
```

### Run ruff formatter
```bash
ruff format addons/
```

## Code Conventions

### XML Views
- Window actions define the model and view modes
- Menu items reference actions via `action=` attribute
- View inheritance uses `inherit_id` and `position` attributes

### File Organization
- Models go in `models/` directory, one model per file
- Views go in `views/` directory
- Security rules go in `security/` as CSV
- Static data goes in `data/` as CSV
- Always register new files in `__manifest__.py` under the `data` key (order matters: security first, then data, then views)

## Linter Configuration

- **Ruff:** line-length 88, Python 3.10 target, Odoo-specific isort sections
- **Pylint:** pylint-odoo plugin enabled, version 19.0
- **Pyright:** includes Odoo 19 source at `/home/rtnet001/odoo19/odoo`

## Key Files Reference

| File | Purpose |
|------|---------|
| `addons/estate/__manifest__.py` | Module metadata, dependencies, data file loading order |
| `addons/estate/models/property.py` | Property model with all field definitions |
| `addons/estate/views/estate_property_views.xml` | Tree and form views for property |
| `addons/estate/security/ir.model.access.csv` | Access control list |
| `config/odoo.conf` | Runtime Odoo configuration |

## Current State

- Single model: `property` with 14 fields (Char, Text, Date, Float, Integer, Boolean, Selection)
- Full CRUD permissions for all internal users
- Basic tree + form views
- Menu structure: Root > First Level > Properties
- `active` field implemented for archive/unarchive functionality
