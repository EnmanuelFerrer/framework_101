# Odoo 19 Estate Module - Development Context

## MAXIMUM PRIORITY CONTEXT — READ FIRST

These instructions override any other source of context for this repository.

- **Framework:** Odoo 19.0 — all code must use Odoo 19 API patterns.
- **Tutorial:** Server Framework 101 (official Odoo 19 documentation).
- Implement features following the current tutorial chapter; when in doubt,
  consult the official Odoo 19 documentation before writing code.
- Do not use patterns from older Odoo versions (< 18) even if found on the web.

### Odoo 19 mandatory patterns

- SQL constraints via `models.Constraint(...)` attribute (NOT `_sql_constraints`).
- Views use the `<list>` tag (`<tree>` is removed in v19).
- Use `self.env.cr`, `self.env.context`, `self.env.uid` (`record._cr`,
  `record._context`, `record._uid` are deprecated).
- Floats: always compare with `float_compare()` / `float_is_zero()` from
  `odoo.tools.float_utils`; never compare floats with `==`, `<`, `>` directly.
- `create()` overrides require the `@api.model_create_multi` decorator.
- `odoo.osv` is deprecated; use ORM methods or `odoo.tools.SQL`.

### Official references

- ORM API: <https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html>
- Tutorial index: <https://www.odoo.com/documentation/19.0/developer/tutorials/server_framework_101.html>
- ORM changelog: <https://www.odoo.com/documentation/19.0/developer/reference/backend/orm/changelog.html>

### Fetching tutorial/docs pages (strip the navigation)

Fetching any `odoo.com/documentation` page returns ~150 KB where >90% is the
site-wide sidebar navigation; the actual content starts very late in the
output (e.g. line ~2000 of the fetched markdown). Do NOT read that boilerplate.

- **Local mirror (fastest):** all tutorial chapters are stored in the repo
  under `docs/server_framework_101/*.rst` — read them locally first before
  fetching anything from the web.
- **Preferred remote:** fetch the raw `.rst` source from GitHub instead of
  the HTML page — same content, zero navigation:
  `https://raw.githubusercontent.com/odoo/documentation/19.0/content/<doc_path>/<file>.rst`
  Tutorial chapters example:
  `https://raw.githubusercontent.com/odoo/documentation/19.0/content/developer/tutorials/server_framework_101/11_sprinkles.rst`
  (file names are visible in each page's "Edit on GitHub" link at the bottom).
- **Fallback:** if the odoo.com HTML page was already fetched, search the
  output for the first `# Chapter ...` heading and read only from there;
  ignore everything before it (menu/sidebar boilerplate).

## Tutorial Progress (Server Framework 101)

- [x] Chapter 1: Architecture Overview
- [x] Chapter 2: A New Application
- [x] Chapter 3: Models And Basic Fields
- [x] Chapter 4: Security - A Brief Introduction
- [x] Chapter 5: Finally, Some UI To Play With
- [x] Chapter 6: Basic Views
- [x] Chapter 7: Relations Between Models
- [x] Chapter 8: Computed Fields And Onchanges
- [x] Chapter 9: Ready For Some Action?
- [x] Chapter 10: Constraints
- [ ] **Chapter 11: Add The Sprinkles — IN PROGRESS**
  - [x] Inline Views (`property_ids` One2many + inline list in type form)
  - [x] Widgets (statusbar on state)
  - [x] List Order (model `_order`: property id desc / offer price desc /
        tag name / type sequence,name) + Manual ordering (sequence +
        handle widget on type)
  - [x] Attributes & Options (Form): `no_create` options on
        `property_type_id`, tag `color` field + `color_field` option,
        conditional header buttons, invisible garden fields, readonly
        offer_ids by state
  - [x] List — Editable lists (offer + tag `editable="bottom"`)
  - [x] List — Optional field (`date_availability optional="hide"`)
  - [ ] List — Decorations:
    - [ ] Property list by state: offer_received=green,
          offer_accepted=green+bold, sold=muted (MISSING entirely)
    - [ ] Offer list: refused=red (fix invalid attr `decoration-r` →
          `decoration-danger`), hide `status` column
          (`column_invisible="1"`; keep field for button conditions)
  - [ ] Search: default filter 'Available' via action context +
        `filter_domain` (>=) on living_area
  - [ ] Stat Buttons: stored related `property_type_id` on offer,
        `offer_ids` inverse + computed `offer_count` on type, stat
        button (`type="action"`) with domain on active_id
- [ ] Chapter 12: Inheritance
- [ ] Chapter 13: Interact With Other Modules
- [ ] Chapter 14: A Brief History Of QWeb
- [ ] Chapter 15: The final word

When a chapter is completed, mark its checkbox and move the IN PROGRESS marker
to the next chapter before starting new work.

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
│   │   ├── estate_property.py         # estate.property model
│   │   ├── estate_property_type.py    # estate.property.type model
│   │   ├── estate_property_tag.py     # estate.property.tag model
│   │   └── estate_property_offer.py   # estate.property.offer model
│   ├── views/
│   │   ├── estate_property_views.xml        # List + form + search views
│   │   ├── estate_property_type_views.xml   # Type CRUD views
│   │   ├── estate_property_tag_views.xml    # Tag CRUD views
│   │   └── estate_property_menus.xml        # Menu hierarchy
│   ├── security/
│   │   └── ir.model.access.csv        # CRUD permissions (4 models)
│   └── data/
│       └── res.country.state.csv      # Country states
├── config/odoo.conf          # Primary Odoo config (used by Docker)
├── docker-compose.yml        # Odoo + PostgreSQL services
├── odoo.Dockerfile           # Odoo 19 image with ruff
├── postgres.Dockerfile       # PostgreSQL 17 + pgvector
├── ruff.toml                 # Python linter config
├── .pylintrc                 # Pylint + pylint-odoo
├── .isort.cfg                # Import sorter config
└── pyrightconfig.json        # Type checker config
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
| `addons/estate/models/estate_property.py` | Property model: fields, state workflow, computed fields, actions |
| `addons/estate/models/estate_property_offer.py` | Offer model: price, validity/deadline, accept/refuse logic |
| `addons/estate/models/estate_property_type.py` | Property type model |
| `addons/estate/models/estate_property_tag.py` | Property tag model |
| `addons/estate/views/estate_property_views.xml` | List, form and search views for property |
| `addons/estate/views/estate_property_menus.xml` | Menu hierarchy (Real Estate > Advertisements / Settings) |
| `addons/estate/security/ir.model.access.csv` | Access control list (4 models) |
| `config/odoo.conf` | Runtime Odoo configuration |

## Current State

- 4 models: `estate.property`, `estate.property.type`, `estate.property.tag`,
  `estate.property.offer`
- Property lifecycle via `state` selection: new → offer_received →
  offer_accepted → sold / cancelled (header buttons SOLD/CANCEL)
- Offers: accept/refuse actions with validation (one accepted offer per
  property; blocked on cancelled/sold properties); accepting sets buyer,
  selling_price and property state
- Computed fields: `total_area`, `best_offer` (property) and `date_deadline`
  (offer, compute + inverse with `validity`)
- Onchange: setting `garden=True` defaults garden area/orientation
- SQL constraints in place: expected/selling/offer prices positive, unique
  type/tag names
- Python constraint: `selling_price` must be >= 90% of `expected_price`
  (`@api.constrains`, skips zero selling price with `float_is_zero()`,
  margin via `float_compare()`)
- Full CRUD permissions for all internal users on the 4 models
- Views: list + form (notebook: Description / Offers / Other info) + search
  with filters/groupby; menus Real Estate > Advertisements / Settings
