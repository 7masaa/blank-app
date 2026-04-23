-- Seed users (hybrid migration decision: recreate users from scratch)
-- Replace password_hash/password_salt with generated PBKDF2 values before production use.

insert into users (email, full_name, role, status, password_hash, password_salt, password_iterations)
values
  ('owner@withelara.com', 'Platform Owner', 'super_admin', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('sofia@withelara.com', 'Sofia', 'super_admin', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('salma@withelara.com', 'Salma', 'cs_lead', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('shelby@withelara.com', 'Shelby', 'affiliate_manager', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('kaija@withelara.com', 'Kaija', 'affiliate_manager', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('roaa@withelara.com', 'Roaa', 'cs_agent', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('mohamed@withelara.com', 'Mohamed', 'engineering', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000)
on conflict (email) do nothing;
