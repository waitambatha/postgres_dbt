-- snapshots/users_snapshot.sql
{% snapshot users_snapshot %}
    {{
        config(
            target_database='my_project_db',
            target_schema='public',
            unique_key='id',
            strategy='timestamp',
            updated_at='created_at'
        )
    }}
    SELECT * FROM users
{% endsnapshot %}