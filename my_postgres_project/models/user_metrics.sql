-- models/user_metrics.sql
SELECT
    COUNT(*) AS total_users,
    AVG(age) AS avg_age
FROM {{ ref('stg_users') }}