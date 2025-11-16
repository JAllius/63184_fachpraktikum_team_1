# DB Init (MySQL 8)

## Prereqs
- MySQL container running (port 3306 on localhost)
- DB/user exist:
  - DB: team1_db
  - User: team1_user / team1_pass

## Create schema
```bash
mysql -h 127.0.0.1 -P 3306 -u team1_user -pteam1_pass team1_db < db/schema_mysql.sql
