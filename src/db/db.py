from __future__ import annotations

import os
import json
import uuid
import contextlib
from typing import Any, Optional, Tuple

import pymysql
from pymysql.cursors import DictCursor

import pandas as pd

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


def get_dataset(dataset_id: str) -> Optional[dict]:
    sql = "SELECT * FROM datasets WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (dataset_id,))
        return cur.fetchone()


# -------------------------------------------------------------------
# DATASET VERSIONS
# -------------------------------------------------------------------

def create_dataset_version(df: pd.DataFrame,
                           dataset_id: str) -> str:
    version_id = str(uuid.uuid4())
    sql = """
        INSERT INTO dataset_versions
        (id, dataset_id, data_json)
        VALUES (%s, %s, %s)
    """
    with cursor() as cur:
        cur.execute(
            sql,
            (
                version_id,
                dataset_id,
                df.to_json(),
            ),
        )
    return version_id


def get_dataset_version(version_id: str) -> Optional[dict]:
    sql = "SELECT * FROM dataset_versions WHERE id = %s"
    with cursor() as cur:
        cur.execute(sql, (version_id,))
        return cur.fetchone()


def get_dataset_version_as_dataframe(version_id: str) -> pd.DataFrame:
    # TODO: implement
    query = get_dataset_version(version_id)
    df = pd.DataFrame(json.loads(query["data_json"]))
    return df
    # get data_json from query
    # build df from data_json
    # return df


# -------------------------------------------------------------------
# ML PROBLEMS
# -------------------------------------------------------------------

def create_ml_problem(
    dataset_version_id: str,
    dataset_version_uri: Optional[str],
    task: str,
    target: str,
    feature_strategy_json: Optional[dict] = None,
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


# -------------------------------------------------------------------
# MODELS
# -------------------------------------------------------------------

def build_model_uri(problem_id: str, model_id: str) -> str:
    # storage-agnostic default
    return f"models/{problem_id}/{model_id}/model.joblib"


def create_model(
    problem_id: str,
    algorithm: str,
    status: str,
    train_mode: Optional[str] = None,
    evaluation_strategy: Optional[str] = None,
    metrics_json: Optional[dict] = None,
    uri: Optional[str] = None,
    metadata_uri: Optional[str] = None,
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
         metrics_json, uri, metadata_uri, explanation_uri, created_by)
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
                metadata_uri,
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
