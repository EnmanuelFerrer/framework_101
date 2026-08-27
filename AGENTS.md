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

> **Audit:** 84 ejercicios verificados contra código fuente (2026-08-27).
> 81 ✅ completados, 2 ⚠️ con desviaciones menores, 1 ❌ pendiente.
> Ver `docs/AUDIT_REPORT.md` para el reporte completo.

- [x] Chapter 1: Architecture Overview (teórico, sin ejercicios)
- [x] Chapter 2: A New Application
  - [x] Create estate module with `__init__.py` and `__manifest__.py`
        (name + base dependency)
  - [x] Make it an 'App' (`application: True`)
- [x] Chapter 3: Models And Basic Fields
  - [x] Create `estate.property` model with `_name` and `_description`
  - [x] Add fields: name(Char,required), description(Text),
        postcode(Char), date_availability(Date), expected_price(Float,
        required), selling_price(Float), bedrooms(Integer),
        living_area(Integer), facades(Integer), garage(Boolean),
        garden(Boolean), garden_area(Integer),
        garden_orientation(Selection: North/South/East/West)
- [x] Chapter 4: Security - A Brief Introduction
  - [x] Create `ir.model.access.csv` with CRUD permissions for
        `base.group_user` on `estate.property`
- [x] Chapter 5: Finally, Some UI To Play With
  - [x] Add `ir.actions.act_window` for `estate.property`
        (`view_mode="list,form"`)
  - [x] Create 3-level menu hierarchy (Real Estate > Advertisements >
        Properties)
  - [x] Set `selling_price` readonly=True
  - [x] Set `date_availability` copy=False, `selling_price` copy=False
  - [x] Default `bedrooms=2`, default `date_availability` = today + 3m
  - [x] Add `active` field with default=True
  - [x] Add `state` field (Selection, 5 values, required, copy=False,
        default='New')
- [x] Chapter 6: Basic Views
  - [x] Custom list view with appropriate fields
  - [x] Custom form view (sheet, groups, notebook with pages)
  - [x] Custom search view with field search shortcuts
  - [x] "Available" filter (state in new/offer_received)
  - [x] "Group By Postcode" (context-based)
- [x] Chapter 7: Relations Between Models
  - [x] `estate.property.type` model with `name` (Char, required)
  - [x] `property_type_id` (Many2one) on property + in views
  - [x] `buyer_id` (Many2one to `res.partner`, copy=False)
  - [x] `salesperson_id` (Many2one to `res.users`, default=current user)
  - [x] `estate.property.tag` model with `name` (Char, required)
  - [x] `tag_ids` (Many2many) with `widget="many2many_tags"`
  - [x] `estate.property.offer` model (price, status, partner_id,
        property_id)
  - [x] `offer_ids` (One2many inverse of `property_id`)
  - [x] Access rights for all 3 new models
- [x] Chapter 8: Computed Fields And Onchanges
  - [x] `total_area` computed (`living_area + garden_area`) with
        `@api.depends`
  - [x] `best_offer` computed (max of offer prices) with `@api.depends`
  - [x] `validity` (Integer, default=7) + `date_deadline` (Date,
        computed + inverse) on offer
  - [x] `date_deadline` = `create_date + validity` days, with inverse
  - [x] `@api.onchange("garden")`: True → area=10/orientation='North';
        False → clear
- [x] Chapter 9: Ready For Some Action?
  - [x] `action_sold` and `action_cancel` methods with UserError guards
  - [x] `action_accept` and `action_refuse` methods on offer
  - [x] Accept sets property buyer_id, selling_price, state to
        offer_accepted
  - [x] Only one accepted offer per property
  - [x] Header buttons in form view
- [x] Chapter 10: Constraints
  - [x] SQL: `CHECK(expected_price > 0)`
  - [x] SQL: `CHECK(selling_price > 0)`
  - [x] SQL: `CHECK(price > 0)` on offer
  - [x] SQL: `unique(name)` on type
  - [x] SQL: `unique(name)` on tag
  - [x] Python: `selling_price >= 90% expected_price` using
        `float_compare`/`float_is_zero`
  - [x] Skip check when `selling_price` is zero
- [x] Chapter 11: Add The Sprinkles
  - [x] Inline list view: `property_ids` on type form (name,
        expected_price, state)
  - [x] `statusbar` widget on `state` field
  - [x] `_order` on all 4 models (property: id desc / offer: price desc
        / tag: name / type: sequence,name)
  - [x] Manual ordering: `sequence` field on type + `handle` widget
  - [x] `no_create` option on `property_type_id`
  - [x] `color` field on tag + `color_field` option on `many2many_tags`
  - [x] Conditional `invisible` on Sold/Cancel header buttons
  - [x] `garden_area`/`garden_orientation` `invisible="not garden"`
  - [x] Accept/Refuse buttons `invisible="status"`
  - [x] `offer_ids` `readonly` when property in
        offer_accepted/sold/cancelled
  - [x] Editable lists for offer and tag (`editable="bottom"`)
  - [x] `date_availability` `optional="hide"`
  - [x] List decorations: property (green/green+bold/muted), offer
        (green accepted/red refused)
  - [x] `status` column `column_invisible="1"` on offer list
  - [x] Default search filter 'Available' via `search_default_available`
  - [x] `filter_domain` on living_area (>= search)
  - [x] Related stored `property_type_id` on offer
  - [x] `offer_count` computed on type
  - [x] Stat button on type form (`type="action"` + `active_id` domain)
- [x] Chapter 12: Inheritance
  - [x] `@api.ondelete`: block deletion if state not new/cancelled
  - [x] `create` override with `@api.model_create_multi` on offer:
        set state to offer_received + validate price
  - [x] `res.users` inheritance with `property_ids` (One2many,
        domain: state=new)
  - [x] View inheritance on `base.view_users_form` with xpath
        (notebook page)
- [x] Chapter 13: Interact With Other Modules
  - [x] `estate_account` link module (depends on `estate` + `account`)
  - [x] Override `action_set_state_sold` with `super()` call
  - [x] Create `account.move` (Customer Invoice) with `partner_id`
        from buyer
  - [x] Invoice lines: 6% of selling price + 100.00 admin fees using
        `Command.create()`
- [x] Chapter 14: A Brief History Of QWeb
  - [x] Minimal kanban view with `name` field, `kanban` in `view_mode`
  - [x] Improved kanban: expected_price, best_price (conditional),
        selling_price (conditional), tags
  - [x] Default grouping by `property_type_id` + prevent drag
- [ ] **Chapter 15: The final word — IN PROGRESS**
  - [ ] Refactor code to match Odoo coding guidelines (lint, naming,
        module structure, XML IDs)
  - [ ] Test on runbot (exploration only, no code)

When a chapter is completed, mark its checkbox and move the IN PROGRESS marker
to the next chapter before starting new work.

## Project Overview

Dockerized Odoo 19 development environment for learning the Server Framework
101 tutorial. Contains a custom addon (`estate`) and a link module
(`estate_account`) for real estate property management.

**Author:** Enmanuel Ferrer

## Project Structure

```text
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
│   │   ├── estate_property_views.xml        # List + form + search + kanban views
│   │   ├── estate_property_type_views.xml   # Type CRUD views + stat button
│   │   ├── estate_property_tag_views.xml    # Tag CRUD views
│   │   ├── estate_property_offer_views.xml  # Offer list (stat button target)
│   │   ├── res_users_views.xml              # Users form inheritance
│   │   └── estate_property_menus.xml        # Menu hierarchy
│   ├── security/
│   │   └── ir.model.access.csv        # CRUD permissions (4 models)
│   └── data/
│       └── res.country.state.csv      # Country states
├── addons/estate_account/   # Link module: estate + account (invoice creation)
│   ├── __manifest__.py      # Depends on estate + account
│   ├── __init__.py
│   └── models/
│       ├── __init__.py
│       └── estate_property.py  # Inherits estate.property, overrides action_set_state_sold
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
- Always register new files in `__manifest__.py` under the `data` key
  (order matters: security first, then data, then views)

## Linter Configuration

- **Ruff:** line-length 88, Python 3.10 target, Odoo-specific isort sections
- **Pylint:** pylint-odoo plugin enabled, version 19.0
- **Pyright:** includes Odoo 19 source at `/home/rtnet001/odoo19/odoo`

## Key Files Reference

| File                                                  | Purpose                                                             |
| ----------------------------------------------------- | ------------------------------------------------------------------- |
| `addons/estate/__manifest__.py`                       | Module metadata, dependencies, data file loading order              |
| `addons/estate/models/estate_property.py`             | Property model: fields, state workflow, computed fields, actions    |
| `addons/estate/models/estate_property_offer.py`       | Offer model: price, validity/deadline, accept/refuse logic          |
| `addons/estate/models/estate_property_type.py`        | Property type model                                                 |
| `addons/estate/models/estate_property_tag.py`         | Property tag model                                                  |
| `addons/estate/models/res_users.py`                   | `res.users` inheritance: adds `property_ids` (available properties) |
| `addons/estate/views/estate_property_views.xml`       | List, form, search and kanban views for property                   |
| `addons/estate/views/estate_property_type_views.xml`  | Type CRUD views + stat button                                       |
| `addons/estate/views/estate_property_tag_views.xml`   | Tag CRUD views                                                      |
| `addons/estate/views/estate_property_offer_views.xml` | Offer list (stat button target)                                     |
| `addons/estate/views/res_users_views.xml`             | Users form view inheritance: property_ids notebook page             |
| `addons/estate/views/estate_property_menus.xml`       | Menu hierarchy (Real Estate > Advertisements / Settings)            |
| `addons/estate/security/ir.model.access.csv`          | Access control list (4 models)                                      |
| `addons/estate_account/__manifest__.py`               | Link module metadata: depends on estate + account                   |
| `addons/estate_account/models/estate_property.py`     | Inherits estate.property, overrides action_set_state_sold           |
| `config/odoo.conf`                                    | Runtime Odoo configuration                                          |

## Current State

- 5 models: `estate.property`, `estate.property.type`, `estate.property.tag`,
  `estate.property.offer`, `res.users` (inherited)
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
- CRUD method overrides: `@api.ondelete` blocks deletion of non-new/cancelled
  properties; offer `create` override sets state to 'Offer Received' and
  blocks lower-price offers
- `estate_account` link module: inherits `estate.property`, overrides
  `action_set_state_sold` with super call (invoice creation pending)
- `res.users` inheritance: `property_ids` (One2many, domain: state='new')
  with notebook page in user form view
- Views: list + form (notebook: Description / Offers / Other info) + search
  with filters/groupby + kanban (grouped by type, no drag); menus
  Real Estate > Advertisements / Settings
- List decorations: property by state (green/green+bold/muted), offer by
  status (green accepted/red refused)
- Editable lists for offer and tag; optional `date_availability` (hidden)
- Default search filter 'Available' via action context; `filter_domain`
  on living_area for `>=` search
- Stat button on property type form: shows offer count, filters offers by
  `property_type_id = active_id` via related stored field
