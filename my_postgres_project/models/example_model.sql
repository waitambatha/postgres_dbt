-- models/example_model.sql
SELECT
    id,
    {{ get_current_timestamp() }} AS processed_at
FROM users