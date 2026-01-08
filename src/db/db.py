from __future__ import annotations

import os
import json
import uuid
import contextlib
from typing import Any, Optional, Tuple, List, Dict, Literal

import pymysql
from pymysql.cursors import DictCursor

# -------------------------------------------------------------------
# MODEL PATH CONFIG
# -------------------------------------------------------------------

MODEL_DIR = os.getenv("MODEL_BASE_PATH", "/models")

# -------------------------------------------------------------------
# DB CONFIG
# -------------------------------------------------------------------

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "team1_db")
DB_USER = os.getenv("DB_USER", "team1_user")
DB_PASS = os.getenv("DB_PASS", "team1_pass")

DB_CFG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASS,
    "database": DB_NAME,
    "autocommit": True,
    "cursorclass": DictCursor,
}


def _json_dump(data: Optional[dict]) -> Optional[str]:
    if data is None:
        return None
    return json.dumps(data)


# -------------------------------------------------------------------
# CONNECTION / CURSOR HELPERS
# -------------------------------------------------------------------

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


# -------------------------------------------------------------------
# USERS
# -------------------------------------------------------------------

def create_user(username: str, email: Optional[str] = None) -> str:
    user_id = str(uuid.uuid4())
    sql = "INSERT INTO users (id, username, email) VALUES (%s, %s, %s)"
    with cursor() as cur:
        cur.execute(sql, (user_id, username, email))
    return user_id


def get_user(user_id: str) -> Optional[dict]:
    sql = "SELECT * FROM users WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (user_id,))
        return cur.fetchone()


# -------------------------------------------------------------------
# DATASETS
# -------------------------------------------------------------------

def create_dataset(name: str, owner_id: Optional[str] = None) -> str:
    dataset_id = str(uuid.uuid4())
    sql = "INSERT INTO datasets (id, name, owner_id) VALUES (%s, %s, %s)"
    with cursor() as cur:
        cur.execute(sql, (dataset_id, name, owner_id))
    return dataset_id


def db_get_dataset(dataset_id: str) -> Optional[dict]:
    sql = "SELECT * FROM datasets WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (dataset_id,))
        return cur.fetchone()
    

ALLOWED_DATASET_SORT_FIELDS = {
    "name": "name",
    "created_at": "created_at",
}

def get_datasets(
    page: int,
    size: int,
    sort: str,
    dir: Literal["asc", "desc"],
    q: Optional[str] = None,
    id: Optional[str] = None,
    name: Optional[str] = None,
) -> Tuple[List[Dict], int]:
    '''
    Return (items, total) for datasets with pagination, sorting and optional search.
    '''
    ### SORTING ###
    sort_column = ALLOWED_DATASET_SORT_FIELDS.get(sort, "created_at")
    dir_sql = "ASC" if dir=="asc" else "DESC"

    ### WHERE CLAUSES - FORMING THE SEARCH QUERIES ###
    where_clauses = []
    params = []

    if q:
        like = f"%{q}%" # Search anything that contains q
        where_clauses.append("name LIKE %s") # If there are more later change name LIKE %s -> (name LIKE %s OR owner_name LIKE %s OR ...)
        params.append(like) # If there are more later swap with .extend and like -> [like, like] -> [like, like, ...]

    if id:
        where_clauses.append("id = %s")
        params.append(id)

    if name:
        like = f"%{name}%" # Search name for anything that contains name
        where_clauses.append("name LIKE %s")
        params.append(like)
    
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    ### TOTAL CALCULATION ###
    count_sql = f"SELECT COUNT(*) AS total FROM datasets {where_sql}"
    with cursor() as cur:
        cur.execute(count_sql, params)
        row = cur.fetchone()
        total = row["total"] if row else 0

    ### RETURN ###
    offset = (page-1)*size
    datasets_sql = f"SELECT * FROM datasets {where_sql} ORDER BY {sort_column} {dir_sql} LIMIT %s OFFSET %s"
    with cursor() as cur:
        cur.execute(datasets_sql, params + [size, offset]) # [size, offset] are not extended in params, so that params is not mutated and only includes the WHERE clauses params
        items = cur.fetchall()

    return items, total

# -------------------------------------------------------------------
# DATASET VERSIONS
# -------------------------------------------------------------------

def create_dataset_version(
    dataset_id: str,
    uri: str,
    name: str | None = None,
    schema_json: Optional[dict] = None,
    profile_json: Optional[dict] = None,
    row_count: Optional[int] = None,
) -> str:
    version_id = str(uuid.uuid4())
    sql = """
        INSERT INTO dataset_versions
        (id, dataset_id, uri, schema_json, profile_json, row_count)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(
            sql,
            (
                version_id,
                dataset_id,
                uri,
                _json_dump(schema_json),
                _json_dump(profile_json),
                row_count,
            ),
        )
    return version_id


def db_get_dataset_version(version_id: str) -> Optional[dict]:
    sql = "SELECT * FROM dataset_versions WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (version_id,))
        return cur.fetchone()


ALLOWED_DATASET_VERSION_SORT_FIELDS = {
    "name": "name",
    "created_at": "created_at",
}


def get_dataset_versions(
    dataset_id: str,
    page: int,
    size: int,
    sort: str,
    dir: Literal["asc", "desc"],
    q: Optional[str] = None,
    id: Optional[str] = None,
    #name: Optional[str] = None,
) -> Tuple[List[Dict], int]:
    '''
    Return (items, total) for dataset_versions for a given dataset_id with pagination, sorting and optional search.
    '''
    ### SORTING ###
    sort_column = ALLOWED_DATASET_VERSION_SORT_FIELDS.get(sort, "created_at")
    dir_sql = "ASC" if dir=="asc" else "DESC"

    ### WHERE CLAUSES - FORMING THE SEARCH QUERIES ###
    where_clauses = []
    params = []

    # if q:
    #     like = f"%{q}%" # Search anything that contains q
    #     where_clauses.append("name LIKE %s") # If there are more later change name LIKE %s -> (name LIKE %s OR owner_name LIKE %s OR ...)
    #     params.append(like) # If there are more later swap with .extend and like -> [like, like] -> [like, like, ...]

    if id:
        where_clauses.append("id = %s")
        params.append(id)

    # if name:
    #     like = f"%{name}%" # Search name for anything that contains name
    #     where_clauses.append("name LIKE %s")
    #     params.append(like)
    
    where_sql = ""
    if where_clauses:
        where_sql = " AND " + " AND ".join(where_clauses)

    ### TOTAL CALCULATION ###
    count_sql = f"SELECT COUNT(*) AS total FROM dataset_versions WHERE dataset_id = %s {where_sql}"
    with cursor() as cur:
        cur.execute(count_sql, [dataset_id] + params)
        row = cur.fetchone()
        total = row["total"] if row else 0

    ### RETURN ###
    offset = (page-1)*size
    dataset_versions_sql = f"SELECT * FROM dataset_versions WHERE dataset_id = %s {where_sql} ORDER BY {sort_column} {dir_sql} LIMIT %s OFFSET %s"
    with cursor() as cur:
        cur.execute(dataset_versions_sql, [dataset_id] + params + [size, offset]) # [size, offset] are not extended in params, so that params is not mutated and only includes the WHERE clauses params
        items = cur.fetchall()

    return items, total


# -------------------------------------------------------------------
# ML PROBLEMS
# -------------------------------------------------------------------

def create_ml_problem(
    dataset_version_id: str,
    task: str,
    target: str,
    name: str = None,
    dataset_version_uri: Optional[str] = None,
    feature_strategy_json: Optional[dict] = "auto",
    schema_snapshot: Optional[dict] = None,
    semantic_types: Optional[dict] = None,
    current_model_id: Optional[str] = None,
) -> str:
    problem_id = str(uuid.uuid4())
    sql = """
        INSERT INTO ml_problems
        (id, dataset_version_id, dataset_version_uri, task, target,
        feature_strategy_json, schema_snapshot, semantic_types, current_model_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(
            sql,
            (
                problem_id,
                dataset_version_id,
                dataset_version_uri,
                task,
                target,
                _json_dump(feature_strategy_json),
                _json_dump(schema_snapshot),
                _json_dump(semantic_types),
                current_model_id,
            ),
        )
    return problem_id


def get_ml_problem(problem_id: str) -> Optional[dict]:
    sql = "SELECT * FROM ml_problems WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (problem_id,))
        return cur.fetchone()
    

ALLOWED_ML_PROBLEM_SORT_FIELDS = {
    "name": "name",
    "task": "task",
    "target": "target",
    "created_at": "created_at",
}


def get_ml_problems(
    dataset_version_id: str,
    page: int,
    size: int,
    sort: str,
    dir: Literal["asc", "desc"],
    q: Optional[str] = None,
    id: Optional[str] = None,
    task: Optional[str] = None,
    target: Optional[str] = None,
    #name: Optional[str] = None,
) -> Tuple[List[Dict], int]:
    '''
    Return (items, total) for dataset_versions for a given dataset_id with pagination, sorting and optional search.
    '''
    ### SORTING ###
    sort_column = ALLOWED_ML_PROBLEM_SORT_FIELDS.get(sort, "created_at")
    dir_sql = "ASC" if dir=="asc" else "DESC"

    ### WHERE CLAUSES - FORMING THE SEARCH QUERIES ###
    where_clauses = []
    params = []

    if q:
        like = f"%{q}%" # Search anything that contains q
        where_clauses.append("task LIKE %s OR target LIKE %s") # If there are more later change name LIKE %s -> (name LIKE %s OR owner_name LIKE %s OR ...)
        params.extend([like, like]) # If there are more later swap with .extend and like -> [like, like] -> [like, like, ...]

    if id:
        where_clauses.append("id = %s")
        params.append(id)

    if task:
        like = f"%{task}%" # Search target for anything that contains target
        where_clauses.append("task LIKE %s")
        params.append(like)

    if target:
        like = f"%{target}%" # Search target for anything that contains target
        where_clauses.append("target LIKE %s")
        params.append(like)
    
    where_sql = ""
    if where_clauses:
        where_sql = " AND " + " AND ".join(where_clauses)

    ### TOTAL CALCULATION ###
    count_sql = f"SELECT COUNT(*) AS total FROM ml_problems WHERE dataset_version_id = %s {where_sql}"
    with cursor() as cur:
        cur.execute(count_sql, [dataset_version_id] + params)
        row = cur.fetchone()
        total = row["total"] if row else 0

    ### RETURN ###
    offset = (page-1)*size
    ml_problems_sql = f"SELECT * FROM ml_problems WHERE dataset_version_id = %s {where_sql} ORDER BY {sort_column} {dir_sql} LIMIT %s OFFSET %s"
    with cursor() as cur:
        cur.execute(ml_problems_sql, [dataset_version_id] + params + [size, offset]) # [size, offset] are not extended in params, so that params is not mutated and only includes the WHERE clauses params
        items = cur.fetchall()

    return items, total


# -------------------------------------------------------------------
# MODELS
# -------------------------------------------------------------------

def build_model_uri(problem_id: str, model_id: str) -> str:
    # storage-agnostic default
    return f"{MODEL_DIR}/{problem_id}/{model_id}/model.joblib"

def create_model(
    problem_id: str,
    algorithm: str,
    status: str,
    train_mode: Optional[str] = None,
    evaluation_strategy: Optional[str] = None,
    metrics_json: Optional[dict] = None,
    uri: Optional[str] = None,         
    metadata_json: Optional[dict] = None,
    explanation_uri: Optional[str] = None,
    created_by: Optional[str] = None,
    name: Optional[str] = None,
) -> Tuple[str, str]:
    model_id = str(uuid.uuid4())

    # Default URI derived from IDs
    if uri is None:
        uri = build_model_uri(problem_id, model_id)

    sql = """
        INSERT INTO models
        (id, problem_id, name, algorithm, train_mode, evaluation_strategy, status,
         metrics_json, uri, metadata_json, explanation_uri, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(
            sql,
            (
                model_id,
                problem_id,
                name,
                algorithm,
                train_mode,
                evaluation_strategy,
                status,
                _json_dump(metrics_json),
                uri,
                _json_dump(metadata_json),
                explanation_uri,
                created_by,
            ),
        )
    return model_id, uri


def get_model(model_id: str) -> Optional[dict]:
    sql = "SELECT * FROM models WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (model_id,))
        return cur.fetchone()


ALLOWED_MODEL_SORT_FIELDS = {
    "name": "name",
    "status": "status",
    "created_at": "created_at",
}


def get_models(
    problem_id: str,
    page: int,
    size: int,
    sort: str,
    dir: Literal["asc", "desc"],
    q: Optional[str] = None,
    id: Optional[str] = None,
    name: Optional[str] = None,
    algorithm: Optional[str] = None,
    train_mode: Optional[str] = None,
    evaluation_strategy: Optional[str] = None,
    status: Optional[str] = None,
) -> Tuple[List[Dict], int]:
    '''
    Return (items, total) for dataset_versions for a given dataset_id with pagination, sorting and optional search.
    '''
    ### SORTING ###
    sort_column = ALLOWED_MODEL_SORT_FIELDS.get(sort, "created_at")
    dir_sql = "ASC" if dir=="asc" else "DESC"

    ### WHERE CLAUSES - FORMING THE SEARCH QUERIES ###
    where_clauses = []
    params = []

    if q:
        like = f"%{q}%" # Search anything that contains q
        where_clauses.append("name LIKE %s OR algorithm LIKE %s OR train_mode LIKE %s OR evaluation_strategy LIKE %s OR status LIKE %s") # If there are more later change name LIKE %s -> (name LIKE %s OR owner_name LIKE %s OR ...)
        params.extend([like, like, like, like, like]) # If there are more later swap with .extend and like -> [like, like] -> [like, like, ...]

    if id:
        where_clauses.append("id = %s")
        params.append(id)

    if name:
        like = f"%{name}%" # Search name for anything that contains name
        where_clauses.append("name LIKE %s")
        params.append(like)

    if algorithm:
        like = f"%{algorithm}%"
        where_clauses.append("algorithm LIKE %s")
        params.append(like)

    if train_mode:
        like = f"%{train_mode}%"
        where_clauses.append("train_mode LIKE %s")
        params.append(like)
    
    if evaluation_strategy:
        like = f"%{evaluation_strategy}%"
        where_clauses.append("evaluation_strategy LIKE %s")
        params.append(like)

    if status:
        like = f"%{status}%"
        where_clauses.append("status LIKE %s")
        params.append(like)
    
    where_sql = ""
    if where_clauses:
        where_sql = " AND " + " AND ".join(where_clauses)

    ### TOTAL CALCULATION ###
    count_sql = f"SELECT COUNT(*) AS total FROM models WHERE problem_id = %s {where_sql}"
    with cursor() as cur:
        cur.execute(count_sql, [problem_id] + params)
        row = cur.fetchone()
        total = row["total"] if row else 0

    ### RETURN ###
    offset = (page-1)*size
    models_sql = f"SELECT * FROM models WHERE problem_id = %s {where_sql} ORDER BY {sort_column} {dir_sql} LIMIT %s OFFSET %s"
    with cursor() as cur:
        cur.execute(models_sql, [problem_id] + params + [size, offset]) # [size, offset] are not extended in params, so that params is not mutated and only includes the WHERE clauses params
        items = cur.fetchall()

    return items, total


# -------------------------------------------------------------------
# JOBS
# -------------------------------------------------------------------

def create_job(
    job_type: str,
    problem_id: Optional[str] = None,
    model_id: Optional[str] = None,
    status: str = "queued",
    task_id: Optional[str] = None,
    requested_by: Optional[str] = None,
) -> str:
    job_id = str(uuid.uuid4())
    sql = """
        INSERT INTO jobs
        (id, type, problem_id, model_id, status, task_id, requested_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(
            sql,
            (job_id, job_type, problem_id, model_id, status, task_id, requested_by),
        )
    return job_id


def update_job_status(job_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Simple status update:
    - if status == 'running'  -> set started_at
    - if status in ('completed', 'failed') -> set finished_at
    - error (if given) is stored
    """
    if status == "running":
        sql = "UPDATE jobs SET status=%s, started_at=NOW(), error=%s WHERE id=%s"
        params = (status, error, job_id)
    elif status in ("completed", "failed"):
        sql = "UPDATE jobs SET status=%s, finished_at=NOW(), error=%s WHERE id=%s"
        params = (status, error, job_id)
    else:
        sql = "UPDATE jobs SET status=%s, error=%s WHERE id=%s"
        params = (status, error, job_id)

    with cursor() as cur:
        cur.execute(sql, params)


def get_job(job_id: str) -> Optional[dict]:
    sql = "SELECT * FROM jobs WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (job_id,))
        return cur.fetchone()


# -------------------------------------------------------------------
# PREDICTIONS
# -------------------------------------------------------------------

def create_prediction(
    model_id: str,
    input_uri: Optional[str] = None,
    inputs_json: Optional[dict] = None,
    outputs_json: Optional[dict] = None,
    outputs_uri: Optional[str] = None,
    requested_by: Optional[str] = None,
) -> str:
    prediction_id = str(uuid.uuid4())
    sql = """
        INSERT INTO predictions
        (id, model_id, input_uri, inputs_json, outputs_json, outputs_uri, requested_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(
            sql,
            (
                prediction_id,
                model_id,
                input_uri,
                _json_dump(inputs_json),
                _json_dump(outputs_json),
                outputs_uri,
                requested_by,
            ),
        )
    return prediction_id


def get_prediction(prediction_id: str) -> Optional[dict]:
    sql = "SELECT * FROM predictions WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (prediction_id,))
        return cur.fetchone()
    

ALLOWED_PREDICTION_SORT_FIELDS = {
    "name": "name",
    "created_at": "created_at",
}


def get_predictions(
    model_id: str,
    page: int,
    size: int,
    sort: str,
    dir: Literal["asc", "desc"],
    q: Optional[str] = None,
    id: Optional[str] = None,
    name: Optional[str] = None,
) -> Tuple[List[Dict], int]:
    '''
    Return (items, total) for predictions for a given dataset_id with pagination, sorting and optional search.
    '''
    ### SORTING ###
    sort_column = ALLOWED_PREDICTION_SORT_FIELDS.get(sort, "created_at")
    dir_sql = "ASC" if dir=="asc" else "DESC"

    ### WHERE CLAUSES - FORMING THE SEARCH QUERIES ###
    where_clauses = []
    params = []

    # if q:
    #     like = f"%{q}%" # Search anything that contains q
    #     where_clauses.append("name LIKE %s") # If there are more later change name LIKE %s -> (name LIKE %s OR owner_name LIKE %s OR ...)
    #     params.append(like) # If there are more later swap with .extend and like -> [like, like] -> [like, like, ...]

    if id:
        where_clauses.append("id = %s")
        params.append(id)

    # if name:
    #     like = f"%{name}%" # Search name for anything that contains name
    #     where_clauses.append("name LIKE %s")
    #     params.append(like)
    
    where_sql = ""
    if where_clauses:
        where_sql = " AND " + " AND ".join(where_clauses)

    ### TOTAL CALCULATION ###
    count_sql = f"SELECT COUNT(*) AS total FROM predictions WHERE model_id = %s {where_sql}"
    with cursor() as cur:
        cur.execute(count_sql, [model_id] + params)
        row = cur.fetchone()
        total = row["total"] if row else 0

    ### RETURN ###
    offset = (page-1)*size
    dataset_versions_sql = f"SELECT * FROM predictions WHERE model_id = %s {where_sql} ORDER BY {sort_column} {dir_sql} LIMIT %s OFFSET %s"
    with cursor() as cur:
        cur.execute(dataset_versions_sql, [model_id] + params + [size, offset]) # [size, offset] are not extended in params, so that params is not mutated and only includes the WHERE clauses params
        items = cur.fetchall()

    return items, total

# -------------------------------------------------------------------
# DASHBOARD STATS
# -------------------------------------------------------------------

def get_dashboard_stats() -> Optional[dict]:
    sql = """
    SELECT
      (SELECT COUNT(*) FROM users)            AS users,
      (SELECT COUNT(*) FROM datasets)         AS datasets,
      (SELECT COUNT(*) FROM dataset_versions) AS dataset_versions,
      (SELECT COUNT(*) FROM ml_problems)      AS ml_problems,
      (SELECT COUNT(*) FROM models)           AS models,
      (SELECT COUNT(*) FROM jobs)             AS jobs,
      (SELECT COUNT(*) FROM predictions)      AS predictions
    """
    with cursor() as cur:
        cur.execute(sql)
        return cur.fetchone()
