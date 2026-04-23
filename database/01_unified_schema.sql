-- Unified platform schema
-- One database, one login, one role model, one extension

create extension if not exists pgcrypto;

create type app_role as enum (
  'super_admin',
  'admin',
  'cs_lead',
  'cs_agent',
  'affiliate_manager',
  'it',
  'engineering',
  'viewer'
);

create type account_status as enum ('pending', 'active', 'disabled');

create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  full_name text not null,
  role app_role not null,
  status account_status not null default 'pending',
  password_hash text not null,
  password_salt text not null,
  password_iterations integer not null default 210000,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  client text not null check (client in ('hub', 'extension', 'admin_dashboard')),
  token_hash text not null,
  expires_at timestamptz not null,
  created_at timestamptz not null default now()
);

create table if not exists folders (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references users(id) on delete cascade,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists snippets (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references users(id) on delete cascade,
  folder_id uuid references folders(id) on delete set null,
  title text not null,
  body text not null,
  status text not null default 'draft' check (status in ('draft', 'submitted', 'approved', 'rejected')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists tickets (
  id uuid primary key default gen_random_uuid(),
  created_by_user_id uuid references users(id) on delete set null,
  assigned_to_user_id uuid references users(id) on delete set null,
  subject text not null,
  priority text not null default 'normal' check (priority in ('low', 'normal', 'high', 'urgent')),
  status text not null default 'open' check (status in ('open', 'in_progress', 'waiting', 'resolved', 'closed')),
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists resources (
  id uuid primary key default gen_random_uuid(),
  key text unique not null,
  label text not null,
  category text not null,
  url text not null,
  min_role app_role not null default 'cs_agent',
  sort_order integer not null default 100,
  created_at timestamptz not null default now()
);

create table if not exists audit_log (
  id bigint generated always as identity primary key,
  actor_user_id uuid references users(id) on delete set null,
  action text not null,
  entity text not null,
  entity_id text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists platform_config (
  key text primary key,
  value jsonb not null,
  updated_at timestamptz not null default now()
);

insert into resources (key, label, category, url, min_role, sort_order)
values
  ('intake_questionnaire', 'Intake Questionnaire', 'CS Workflow', 'https://docs.google.com/spreadsheets/d/1Lt0roLGLJocjb5r7qkm91Z1IBBUDo0u2K8uyk-2I22Q/edit?pli=1&gid=132844709#gid=132844709', 'cs_agent', 10),
  ('meds_storage', 'Meds Storage Instructions', 'CS Workflow', 'https://docs.google.com/spreadsheets/d/1BIIDiCuqwuEiQED-yErBATd2W3rwQt3EESZ3INp4SFk/edit?gid=1979052169#gid=1979052169', 'cs_agent', 20),
  ('faq', 'FAQ', 'Knowledge Base', 'https://docs.google.com/document/d/1HW-0Ubc2IWQ34enuQB9QqG7iVvSYCdDn/edit', 'cs_agent', 30),
  ('med_training', 'Med Training', 'Knowledge Base', 'https://docs.google.com/document/d/15G0Dq_PBOo45XsXVCJdWxlfIC5Ab2XbZ/edit', 'cs_agent', 40),
  ('comm_standards', 'Communication Standards', 'Knowledge Base', 'https://docs.google.com/document/d/10NxCAFk_i_6vao90B0M-i-RU7bmJE_TsKVjAcBtM-G4/edit?tab=t.0', 'cs_agent', 50),
  ('upsell_playbook', 'Upsell Playbook', 'Sales', 'https://docs.google.com/document/d/1LzTseXMGf6ApXwkZ3LG77S1-s78UOZSq/edit', 'cs_agent', 60),
  ('pricing', 'Pricing', 'Sales', 'https://affiliate.withelara.com/resources', 'affiliate_manager', 70)
on conflict (key) do nothing;
