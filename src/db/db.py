# src/db/db.py
from __future__ import annotations
import os, json, contextlib
import pymysql

DB_CFG = dict(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "team1_user"),
    password=os.getenv("DB_PASS", "team1_pass"),
    database=os.getenv("DB_NAME", "team1_db"),
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
)

def get_conn():
    return pymysql.connect(**DB_CFG)

@contextlib.contextmanager
def cursor():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            yield cur
    finally:
        conn.close()

# ---------- datasets ----------
def create_dataset(name: str, owner: str | None = None) -> int:
    sql = "INSERT INTO datasets (name, owner) VALUES (%s, %s)"
    with cursor() as cur:
        cur.execute(sql, (name, owner))
        return cur.lastrowid

def get_dataset(dataset_id: int) -> dict | None:
    with cursor() as cur:
        cur.execute("SELECT * FROM datasets WHERE id=%s", (dataset_id,))
        return cur.fetchone()

# ------ dataset_versions ------
def create_dataset_version(
    dataset_id: int, uri: str,
    schema_json: dict | None = None,
    profile_json: dict | None = None,
    row_count: int | None = None,
) -> int:
    sql = """
        INSERT INTO dataset_versions (dataset_id, uri, schema_json, profile_json, row_count)
        VALUES (%s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(sql, (
            dataset_id, uri,
            json.dumps(schema_json) if schema_json else None,
            json.dumps(profile_json) if profile_json else None,
            row_count,
        ))
        return cur.lastrowid

def get_dataset_version(version_id: int) -> dict | None:
    with cursor() as cur:
        cur.execute("SELECT * FROM dataset_versions WHERE id=%s", (version_id,))
        return cur.fetchone()

# --------- ml_problems ---------
def create_ml_problem(
    dataset_version_id: int, task: str, target: str,
    feature_strategy_json: dict | None = None,
    validation_strategy: str | None = None,
) -> int:
    sql = """
        INSERT INTO ml_problems
        (dataset_version_id, task, target, feature_strategy_json, validation_strategy)
        VALUES (%s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(sql, (
            dataset_version_id, task, target,
            json.dumps(feature_strategy_json) if feature_strategy_json else None,
            validation_strategy,
        ))
        return cur.lastrowid

def get_ml_problem(problem_id: int) -> dict | None:
    with cursor() as cur:
        cur.execute("SELECT * FROM ml_problems WHERE id=%s", (problem_id,))
        return cur.fetchone()

# ------------ models ------------
def save_model_metadata(
    problem_id: int, framework_algorithm: str, status: str,
    metrics_json: dict | None = None, model_uri: str | None = None,
    name: str | None = None,
) -> int:
    sql = """
        INSERT INTO models
        (problem_id, name, framework_algorithm, status, metrics_json, model_uri)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(sql, (
            problem_id, name, framework_algorithm, status,
            json.dumps(metrics_json) if metrics_json else None,
            model_uri,
        ))
        return cur.lastrowid

def get_model(model_id: int) -> dict | None:
    with cursor() as cur:
        cur.execute("SELECT * FROM models WHERE id=%s", (model_id,))
        return cur.fetchone()

# -------------- jobs --------------
def create_job(job_type: str, problem_id: int | None = None,
               model_id: int | None = None, status: str = "queued") -> int:
    sql = "INSERT INTO jobs (type, problem_id, model_id, status) VALUES (%s,%s,%s,%s)"
    with cursor() as cur:
        cur.execute(sql, (job_type, problem_id, model_id, status))
        return cur.lastrowid

def update_job_status(job_id: int, status: str, error: str | None = None) -> None:
    if error:
        sql = "UPDATE jobs SET status=%s, error=%s, finished_at=NOW() WHERE id=%s"
        params = (status, error, job_id)
    elif status == "running":
        sql = "UPDATE jobs SET status=%s, started_at=NOW() WHERE id=%s"
        params = (status, job_id)
    elif status in ("completed", "failed"):
        sql = "UPDATE jobs SET status=%s, finished_at=NOW() WHERE id=%s"
        params = (status, job_id)
    else:
        sql = "UPDATE jobs SET status=%s WHERE id=%s"
        params = (status, job_id)
    with cursor() as cur:
        cur.execute(sql, params)

def get_job(job_id: int) -> dict | None:
    with cursor() as cur:
        cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
        return cur.fetchone()

# ----------- predictions ----------
def save_prediction(
    problem_id: int, model_id: int, job_id: int | None = None,
    inputs_json: dict | None = None, outputs_json: dict | None = None,
    outputs_uri: str | None = None,
) -> int:
    sql = """
        INSERT INTO predictions
        (problem_id, model_id, job_id, inputs_json, outputs_json, outputs_uri)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(sql, (
            problem_id, model_id, job_id,
            json.dumps(inputs_json) if inputs_json else None,
            json.dumps(outputs_json) if outputs_json else None,
            outputs_uri,
        ))
        return cur.lastrowid

def get_prediction(pred_id: int) -> dict | None:
    with cursor() as cur:
        cur.execute("SELECT * FROM predictions WHERE id=%s", (pred_id,))
        return cur.fetchone()
