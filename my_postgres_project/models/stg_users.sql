-- models/stg_users.sql
SELECT
    id,
    first_name,
    last_name,
    email,
    age,
    created_at
FROM users
WHERE age >= 18