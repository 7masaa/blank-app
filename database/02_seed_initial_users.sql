-- Seed users (hybrid migration decision: recreate users from scratch)
-- Replace password_hash/password_salt with generated PBKDF2 values before production use.

insert into users (email, full_name, role, status, password_hash, password_salt, password_iterations)
values
  ('info@withelara.com', 'Platform Owner', 'super_admin', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('sofia@withelara.com', 'Sofia', 'super_admin', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('support@withelara.com', 'Salma', 'cs_lead', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('connect@withelara.com', 'Shelby', 'affiliate_manager', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('kaija.marketing@withelara.com', 'Kaija', 'affiliate_manager', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('haneenhamed618@gmail.com', 'Haneen', 'cs_agent', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000),
  ('systems@withelara.com', 'Mohamed', 'engineering', 'active', 'REPLACE_ME', 'REPLACE_ME', 210000)
on conflict (email) do nothing;
