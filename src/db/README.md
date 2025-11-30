Database Setup & Scripts (MySQL 8)

This folder contains everything needed to create and verify the database for our Predictive Analytics service (FastAPI + MySQL).

1) What each script/file does

src/db/schema_mysql.sql – Creates all tables (users, datasets, dataset_versions, ml_problems, models, jobs, predictions).

IDs are UUID strings (CHAR(36)).

evaluation_strategy lives on models (not ml_problems).

src/db/seed.sql – Optional local-only seed script (UUID-based).

It inserts a tiny demo graph and then TRUNCATES all tables at the end (so it acts like a “seed self-test” and leaves the DB empty).

src/db/init_db.py – Python runner that connects to MySQL and applies the schema (and optionally seed).

src/db/db.py – DB helper functions used by the API (create/read users, datasets, versions, problems, models, jobs, predictions).

Prediction helper is create_prediction (legacy alias save_prediction may exist during transition).

src/db/test_smoke.py – Local smoke test that runs the happy-path using db.py (quick verification).

2) Prerequisites

Docker + Docker Compose running.

MySQL container exposed on 127.0.0.1:3306.

Recommended persistence in docker-compose.yml:

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: safe123
      MYSQL_DATABASE: team1_db
      MYSQL_USER: team1_user
      MYSQL_PASSWORD: team1_pass
    ports:
      - "3306:3306"
    volumes:
      - db-data:/var/lib/mysql
volumes:
  db-data:

3) Initialize / Recreate the schema

Apply the schema (creates tables if missing):

python src/db/init_db.py


Note: the schema uses CREATE TABLE IF NOT EXISTS. If you change columns, you must either drop tables (or the database) and re-run init, or write a migration.

Drop tables manually (dev reset)
mysql -h 127.0.0.1 -P 3306 -u team1_user -pteam1_pass team1_db -e "
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS ml_problems;
DROP TABLE IF EXISTS dataset_versions;
DROP TABLE IF EXISTS datasets;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS=1;
"
python src/db/init_db.py

4) Run the local smoke test

The smoke test is meant for local verification only. It skips automatically if:

PYTEST_CI_MODE=True, or

MySQL is not reachable.

Run:

```bash
unset PYTEST_CI_MODE
PYTHONPATH=. pytest -q src/db/test_smoke.py -s
```

5) (Optional) Run seed.sql

Seed is local-only and currently works like a self-test:

inserts demo rows

then truncates everything at the end (DB ends empty)

Run it directly:

```bash
mysql -h 127.0.0.1 -P 3306 -u team1_user -pteam1_pass team1_db < src/db/seed.sql
```

6) Create & populate a test database (team1_db_test)

We use a separate database `team1_db_test` for end-to-end pipeline testing (so we don’t mess with `team1_db` demo/dev data).

### One-time setup (needs MySQL root)
If you don't have permissions to create databases with `team1_user`, create the test DB once using root (root password is from `docker-compose.yml`):

```bash
mysql -h 127.0.0.1 -P 3306 -u root -psafe123 -e "CREATE DATABASE IF NOT EXISTS team1_db_test;"
mysql -h 127.0.0.1 -P 3306 -u root -psafe123 -e "GRANT ALL PRIVILEGES ON team1_db_test.* TO 'team1_user'@'%'; FLUSH PRIVILEGES;"
```

Populate test DB (1 row per table)

This script applies the schema to team1_db_test, optionally resets tables, and inserts exactly 1 row per table. It also copies the first entries from src/db/test_db.txt into dataset_versions and ml_problems.

Run from repo root:

```bash
python -m src.db.init_test_db --reset
```

Run helpers/tests against the test DB

Because db.py reads DB_NAME from env, you can run anything against the test DB like this:

```bash
DB_NAME=team1_db_test PYTHONPATH=. pytest -q src/db/test_smoke.py -s

