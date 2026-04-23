-- Optional migration helpers for hybrid plan:
-- Keep snippets + tickets, recreate users in new DB.

-- 1) Export snippets from legacy snippet database.
-- select id, title, content as body, created_at, updated_at from legacy_snippets;

-- 2) Export tickets from legacy ticket database.
-- select id, subject, priority, status, payload, created_at, updated_at from legacy_tickets;

-- 3) Import snippets/tickets and map users by email.
-- Example:
-- insert into snippets (id, owner_user_id, title, body, created_at, updated_at)
-- select ls.id, u.id, ls.title, ls.body, ls.created_at, ls.updated_at
-- from staging_legacy_snippets ls
-- join users u on u.email = ls.owner_email;

-- insert into tickets (id, created_by_user_id, assigned_to_user_id, subject, priority, status, payload, created_at, updated_at)
-- select lt.id, u1.id, u2.id, lt.subject, lt.priority, lt.status, lt.payload, lt.created_at, lt.updated_at
-- from staging_legacy_tickets lt
-- left join users u1 on u1.email = lt.created_by_email
-- left join users u2 on u2.email = lt.assigned_to_email;
