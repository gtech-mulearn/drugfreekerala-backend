# Setup

1. run following to up
   `docker compose up --build -d`
2. Setup .env file reffer .env.sample
3. run following to create tables
   `docker compose exec backend python init.py`

NOTE: Adjust number of workers in docker-compose.yml file as per your system configuration. deffault is 2 workers.

# Migrations

`init.py` only creates tables that don't exist yet; it never changes an existing one.
On a database that already has data, run each file in `db/migrations/` once, in date order,
**before** deploying the code that needs it.

# Tests

```
pip install -r requirements-dev.txt
pytest
```

The tests use an in-memory SQLite database, so they never touch MySQL.
