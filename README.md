# Unified Role-Based Internal System

A modernized Streamlit control hub with:

- Role-based login and gated tooling
- Embedded resource webviews (iframe-first)
- Unified schema and migration SQL for one Supabase DB
- Single-extension scaffold for snippets/tickets/resources

## App file

If your Streamlit Cloud app uses a renamed entrypoint (for example `internal_system_app.py`), set that path in Streamlit Cloud settings.

Default entrypoint in this repo:

- `streamlit_app.py`

## Demo login

All demo users use password: `demo1234`

- `owner@withelara.com`
- `salma@withelara.com`
- `roaa@withelara.com`
- `shelby@withelara.com`
- `info@withelara.com`

## Local run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Project structure

- `streamlit_app.py` — upgraded hub UI and embedded webview resources
- `database/01_unified_schema.sql` — unified DB schema + seeded resources
- `database/02_seed_initial_users.sql` — seed template for initial users
- `database/03_optional_migrate_data.sql` — optional migration helper
- `extension/` — unified extension scaffold
- `SETUP.md` — setup and rollout notes
