# Database Setup & Scripts (MySQL 8)

This folder contains everything to create, initialize, the database for our Predictive Analytics service.

## 1) What each script/file does
- **`src/db/schema_mysql.sql`** – Creates all tables (`datasets`, `dataset_versions`, `ml_problems`, `models`, `jobs`, `predictions`).
- **`src/db/seed.sql`** – Inserts tiny demo rows (optional; for local testing only) --> set  main(apply_seed=True) in init_db.py to enable it.
- **`src/db/init_db.py`** – Python runner that connects to MySQL and applies **schema** (and **seed** if enabled).
- **`src/db/db.py`** – DB helper functions used by the API (create/read datasets, versions, problems, jobs, models, predictions).
- **`src/db/test_smoke.py`** – Small local smoke test that uses `db.py` to insert/read rows (for quick verification).

## 2) Prerequisites
- Docker + Docker Compose running.
- MySQL container exposed on `127.0.0.1:3306`.
- Recommended persistence in `docker-compose.yml`:
  ```yaml
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
