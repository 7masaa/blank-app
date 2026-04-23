# Unified Role-Based Platform Foundation

This repo now contains a practical foundation for the system you requested:

- **One DB schema** for users, sessions, snippets, tickets, resources, config, and audit
- **One role model** (`super_admin`, `admin`, `cs_lead`, `cs_agent`, `affiliate_manager`, `it`, `engineering`, `viewer`)
- **One login concept** shared across hub and extension
- **One extension scaffold** with keyboard shortcuts and tabbed popup
- **One role-gated hub demo** implemented in Streamlit

## Repository layout

- `database/01_unified_schema.sql` - unified schema + seeded CS resource links
- `database/02_seed_initial_users.sql` - initial users to recreate accounts in new DB
- `database/03_optional_migrate_data.sql` - hybrid migration helper for snippets/tickets
- `extension/*` - single-extension scaffold (manifest, background, popup)
- `streamlit_app.py` - role-based login + resource access demo
- `SETUP.md` - deployment and rollout steps

## Run the hub demo

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
