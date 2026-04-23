# Setup and Rollout Guide

## 1) Provision new Supabase project

1. Create a fresh Supabase project.
2. Run `database/01_unified_schema.sql`.
3. Generate PBKDF2 hashes for real passwords.
4. Update `database/02_seed_initial_users.sql` and run it.

## 2) Migrate legacy data (hybrid plan)

- Recreate users from scratch in new DB.
- Export snippets and tickets from legacy systems into staging tables.
- Use patterns in `database/03_optional_migrate_data.sql` to import snippets/tickets and map by user email.

## 3) Configure website (hub)

- The `streamlit_app.py` file is a role-gated hub demo.
- Replace in-memory users with database-backed auth endpoints.
- Replace static resource list with `resources` table query.

## 4) Configure extension

- Load `extension/` as an unpacked extension in Chrome.
- Verify shortcuts:
  - Cmd/Ctrl+Shift+E: open extension
  - Cmd/Ctrl+Shift+S: snippets tab
  - Cmd/Ctrl+Shift+T: tickets tab
  - Cmd/Ctrl+Shift+R: resources tab
- Connect popup/account screens to Supabase session APIs.

## 5) Security checklist

- Enforce HTTPS only.
- Rotate salts/tokens for all seeded users.
- Add rate limiting and lockout policies.
- Add audit logging for login, role change, and data export events.
