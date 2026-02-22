# Database (MySQL 8) – Setup & DB Scripts

This folder contains the database schema and helper scripts for PAaaS (FastAPI + MySQL 8).  
Goal: make the DB setup and verification reproducible for new team members.

## What is in this folder?

- `schema_mysql.sql`  
  Creates all DB tables (users, datasets, dataset_versions, ml_problems, models, jobs, predictions).

- `init_db.py`  
  Applies the schema to the configured database (idempotent because of `CREATE TABLE IF NOT EXISTS`).

- `db.py`  
  Python DB layer used by the API: CRUD helpers, joins for detail views, pagination/filtering, and the production-model switch.

- `seed.sql`  
  Optional local seed/self-test script. (May insert demo rows; use for manual checks.)
  This script ends with TRUNCATE (DB ends empty)

- `test_smoke.py`  
  Local smoke test that verifies schema + CRUD + joins + pagination + deletes + production switch.

## Prerequisites

- Docker + Docker Compose
- MySQL service reachable from the API (via docker network name `db`)
- Default environment variables (from docker-compose):
  - `DB_HOST=db`
  - `DB_PORT=3306`
  - `DB_NAME=team1_db`
  - `DB_USER=team1_user`
  - `DB_PASS=team1_pass`

## Quick start (recommended)

### Fresh start (clean DB)
```bash
docker compose down -v
docker compose up -d --build

