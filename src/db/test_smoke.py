# src/db/test_smoke.py
from __future__ import annotations

import os
import uuid
import pytest
import pymysql

from ..db import init_db
from ..db.db import (
    # Core create/read
    create_user,
    get_user,
    create_dataset,
    db_get_dataset,
    create_dataset_version,
    db_get_dataset_version,
    create_ml_problem,
    get_ml_problem,
    create_model,
    get_model,
    create_job,
    get_job,
    create_prediction,
    get_prediction,
    # Updates
    update_dataset,
    update_dataset_version,
    update_ml_problem,
    update_model,
    update_prediction,
    # Lists (pagination/filtering)
    get_datasets,
    get_dataset_versions,
    get_ml_problems,
    get_models,
    get_predictions,
    # Detail joins
    get_dataset_version_detail,
    get_ml_problem_detail,
    get_model_detail,
    # Joined list functions
    get_dataset_versions_all_joined,
    get_ml_problems_all_joined,
    get_models_all_joined,
    get_predictions_all_joined,
    get_ml_predictions_all_joined,
    # Stats
    get_dashboard_stats,
    # Deletes (manual cascades)
    delete_prediction,
    delete_job,
    delete_model,
    delete_ml_problem,
    delete_dataset_version,
    delete_dataset,
    # Transaction
    set_model_to_production,
)

# ---------------------------------------------------------
# Local-only: skip in CI (no DB service there)
# ---------------------------------------------------------
if os.getenv("PYTEST_CI_MODE") == "True":
    pytest.skip("Skipping DB smoke tests in CI (no MySQL service).", allow_module_level=True)


def _db_connect_kwargs():
    return dict(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "team1_user"),
        password=os.getenv("DB_PASS", "team1_pass"),
        database=os.getenv("DB_NAME", "team1_db"),
        connect_timeout=3,
        autocommit=True,
    )


def _can_connect() -> bool:
    try:
        conn = pymysql.connect(**_db_connect_kwargs())
        conn.close()
        return True
    except Exception:
        return False


if not _can_connect():
    pytest.skip("Skipping DB smoke tests (MySQL not reachable).", allow_module_level=True)


def _truncate_all_tables() -> None:
    """Reset tables so tests are reproducible (same result on every machine)."""
    conn = pymysql.connect(**_db_connect_kwargs())
    try:
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS=0;")
            for t in ["predictions", "jobs", "models", "ml_problems", "dataset_versions", "datasets", "users"]:
                cur.execute(f"TRUNCATE TABLE {t};")
            cur.execute("SET FOREIGN_KEY_CHECKS=1;")
    finally:
        conn.close()


def _print_test(title: str) -> None:
    # Short prints that show progress when running: pytest -s
    print(f"\n[DB SMOKE] {title}")


# ---------------------------------------------------------
# Fixture: ensure schema exists (idempotent)
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def ensure_schema():
    # Safe because schema uses CREATE TABLE IF NOT EXISTS.
    os.environ.setdefault("SCHEMA_PATH", "src/db/schema_mysql.sql")
    os.environ.setdefault("SEED_PATH", "/dev/null")
    init_db.main(apply_seed=False)
    yield


@pytest.fixture(autouse=True)
def clean_db():
    _truncate_all_tables()
    yield


# ---------------------------------------------------------
# 1) Core CRUD + joins + dashboard stats
# ---------------------------------------------------------
def test_smoke_core_crud_joins_and_stats():
    _print_test("Core CRUD + joins + dashboard stats")

    # Create
    user_id = create_user("smoke_user", "smoke@example.com")
    assert get_user(user_id)["id"] == user_id

    ds_id = create_dataset("smoke_dataset", owner_id=user_id)
    assert db_get_dataset(ds_id)["id"] == ds_id

    dv_id = create_dataset_version(
        dataset_id=ds_id,
        uri="/data/smoke.csv",
        name="smoke_version_1",
        filename="smoke.csv",
        schema_json={"x": "int64", "y": "int64"},
        profile_json={"summary": {"n_rows": 10}},
        row_count=10,
    )
    assert db_get_dataset_version(dv_id)["id"] == dv_id

    prob_id = create_ml_problem(
        dataset_version_id=dv_id,
        task="classification",
        target="y",
        name="smoke_problem_1",
        dataset_version_uri="/data/smoke.csv",
        feature_strategy_json={"mode": "auto"},
        schema_snapshot={"x": "int64", "y": "int64"},
        semantic_types={"numeric": ["x"], "categorical": [], "boolean": []},
        current_model_id=None,
    )
    assert get_ml_problem(prob_id)["id"] == prob_id

    model_id, model_uri = create_model(
        problem_id=prob_id,
        algorithm="dummy_algorithm",
        status="staging",
        name="smoke_model_1",
        train_mode="auto",
        evaluation_strategy="train_test_split",
        metrics_json={"acc": 0.9},
        uri=None,  # default URI will be generated
        metadata_json=None,
        explanation_json=None,
        created_by=user_id,
    )
    assert get_model(model_id)["id"] == model_id
    assert isinstance(model_uri, str) and len(model_uri) > 0

    job_id = create_job(
        job_type="train",
        problem_id=prob_id,
        model_id=model_id,
        status="queued",
        task_id="celery-task-123",
        requested_by=user_id,
    )
    assert get_job(job_id)["id"] == job_id

    pred_id = create_prediction(
        name="smoke_prediction_1",
        model_id=model_id,
        input_uri="/data/smoke_inputs.json",
        inputs_json={"x": 42},
        outputs_json={"y_hat": 0.8},
        outputs_uri="/outputs/smoke_pred.json",
        status="completed",  # schema requires status
        requested_by=user_id,
    )
    assert get_prediction(pred_id)["id"] == pred_id

    # Updates (prove dynamic UPDATE builder works)
    assert update_dataset(ds_id, name="smoke_dataset_renamed") is True
    assert db_get_dataset(ds_id)["name"] == "smoke_dataset_renamed"

    assert update_dataset_version(dv_id, name="smoke_version_renamed", row_count=11) is True
    dv = db_get_dataset_version(dv_id)
    assert dv["name"] == "smoke_version_renamed"
    assert int(dv["row_count"]) == 11

    assert update_ml_problem(prob_id, name="smoke_problem_renamed") is True
    assert get_ml_problem(prob_id)["name"] == "smoke_problem_renamed"

    assert update_model(model_id, status="archived", name="smoke_model_archived") is True
    m = get_model(model_id)
    assert m["status"] == "archived"
    assert m["name"] == "smoke_model_archived"

    assert update_prediction(pred_id, status="failed") is True
    assert get_prediction(pred_id)["status"] == "failed"

    # Join detail helpers (prove lineage joins work)
    dv_detail = get_dataset_version_detail(dv_id)
    assert dv_detail["dataset_name"] == "smoke_dataset_renamed"

    prob_detail = get_ml_problem_detail(prob_id)
    assert prob_detail["dataset_name"] == "smoke_dataset_renamed"
    assert prob_detail["dataset_version_id"] == dv_id

    model_detail = get_model_detail(model_id)
    assert model_detail["dataset_name"] == "smoke_dataset_renamed"
    assert model_detail["problem_task"] == "classification"
    assert model_detail["problem_target"] == "y"

    # Dashboard stats (counts should reflect what we created)
    stats = get_dashboard_stats()
    assert stats["users"] == 1
    assert stats["datasets"] == 1
    assert stats["dataset_versions"] == 1
    assert stats["ml_problems"] == 1
    assert stats["models"] == 1
    assert stats["jobs"] == 1
    assert stats["predictions"] == 1


# ---------------------------------------------------------
# 2) List functions (pagination/filtering) + joined list functions
# ---------------------------------------------------------
def test_smoke_lists_and_joined_lists():
    _print_test("List functions + joined list functions")

    user_id = create_user("list_user", "list@example.com")

    # Create multiple datasets so pagination/filtering is meaningful
    ds_a = create_dataset("alpha_dataset", owner_id=user_id)
    ds_b = create_dataset("beta_dataset", owner_id=user_id)
    ds_g = create_dataset("gamma_dataset", owner_id=user_id)

    # Dataset list: q + pagination
    items, total = get_datasets(page=1, size=2, sort="created_at", dir="desc", q="a", id=None, name=None)
    assert total >= 2
    assert 0 < len(items) <= 2

    # Create versions for one dataset and test dataset_versions list
    dv1 = create_dataset_version(ds_a, uri="/data/a1.csv", name="v1", filename="a1.csv", schema_json={}, profile_json={}, row_count=1)
    dv2 = create_dataset_version(ds_a, uri="/data/a2.csv", name="v2", filename="a2.csv", schema_json={}, profile_json={}, row_count=2)

    v_items, v_total = get_dataset_versions(dataset_id=ds_a, page=1, size=10, sort="created_at", dir="desc", q=None, id=None, name=None)
    assert v_total == 2
    assert len(v_items) == 2

    # Create ML problems and test ml_problems list
    p1 = create_ml_problem(dataset_version_id=dv1, task="classification", target="y", name="p1", dataset_version_uri="/data/a1.csv")
    p2 = create_ml_problem(dataset_version_id=dv1, task="regression", target="y", name="p2", dataset_version_uri="/data/a1.csv")

    p_items, p_total = get_ml_problems(dataset_version_id=dv1, page=1, size=10, sort="created_at", dir="desc", q=None, id=None, task=None, target=None, name=None)
    assert p_total == 2
    assert len(p_items) == 2

    # Create models and test models list
    m1, _ = create_model(problem_id=p1, algorithm="algo1", status="staging", name="m1", created_by=user_id)
    m2, _ = create_model(problem_id=p1, algorithm="algo2", status="staging", name="m2", created_by=user_id)

    m_items, m_total = get_models(problem_id=p1, page=1, size=10, sort="created_at", dir="desc", q=None, id=None, name=None,
                                  algorithm=None, train_mode=None, evaluation_strategy=None, status=None)
    assert m_total == 2
    assert len(m_items) == 2

    # Create predictions and test predictions list
    pr1 = create_prediction(name="pred1", model_id=m1, input_uri="/in/1.json", inputs_json={}, outputs_json={}, outputs_uri="/out/1.json", status="completed", requested_by=user_id)
    pr2 = create_prediction(name="pred2", model_id=m1, input_uri="/in/2.json", inputs_json={}, outputs_json={}, outputs_uri="/out/2.json", status="completed", requested_by=user_id)

    pr_items, pr_total = get_predictions(model_id=m1, page=1, size=10, sort="created_at", dir="desc", q=None, id=None, name=None)
    assert pr_total == 2
    assert len(pr_items) == 2

    # Joined list functions (sanity: totals >= what we inserted)
    jv_items, jv_total = get_dataset_versions_all_joined(page=1, size=50, sort="created_at", dir="desc", q=None, dataset_name=None, version_name=None)
    assert jv_total >= 2
    assert len(jv_items) >= 2

    jp_items, jp_total = get_ml_problems_all_joined(page=1, size=50, sort="created_at", dir="desc", q=None, id=None, task=None, target=None,
                                                    dataset_name=None, dataset_version_name=None, problem_name=None)
    assert jp_total >= 2
    assert len(jp_items) >= 2

    jm_items, jm_total = get_models_all_joined(page=1, size=50, sort="created_at", dir="desc", q=None, id=None, name=None, algorithm=None,
                                               train_mode=None, evaluation_strategy=None, status=None, problem_name=None, dataset_version_name=None, dataset_name=None)
    assert jm_total >= 2
    assert len(jm_items) >= 2

    jpr_items, jpr_total = get_predictions_all_joined(page=1, size=50, sort="created_at", dir="desc", q=None, id=None, name=None, status=None,
                                                      model_name=None, problem_name=None, dataset_version_name=None, dataset_name=None)
    assert jpr_total >= 2
    assert len(jpr_items) >= 2

    # Predictions by problem (joined)
    ppr_items, ppr_total = get_ml_predictions_all_joined(problem_id=p1, page=1, size=50, sort="created_at", dir="desc", q=None, name=None, status=None, model_name=None)
    assert ppr_total == 2
    assert len(ppr_items) == 2


# ---------------------------------------------------------
# 3) Transaction: set_model_to_production (row lock + consistent state)
# ---------------------------------------------------------
def test_smoke_set_model_to_production_transaction():
    _print_test("Transaction: set_model_to_production")

    user_id = create_user("prod_user", "prod@example.com")
    ds_id = create_dataset("prod_dataset", owner_id=user_id)

    dv_id = create_dataset_version(
        dataset_id=ds_id,
        uri="/data/prod.csv",
        name="prod_version_1",
        filename="prod.csv",
        schema_json={"x": "int64", "y": "int64"},
        profile_json={"summary": {"n_rows": 5}},
        row_count=5,
    )

    prob_id = create_ml_problem(
        dataset_version_id=dv_id,
        task="regression",
        target="y",
        name="prod_problem_1",
        dataset_version_uri="/data/prod.csv",
        current_model_id=None,
    )

    m1, _ = create_model(problem_id=prob_id, name="m1", algorithm="algo1", status="staging", created_by=user_id)
    m2, _ = create_model(problem_id=prob_id, name="m2", algorithm="algo2", status="staging", created_by=user_id)

    # First switch
    assert set_model_to_production(prob_id, m1) is True
    assert get_ml_problem(prob_id)["current_model_id"] == m1
    assert get_model(m1)["status"] == "production"

    # Second switch (old archived)
    assert set_model_to_production(prob_id, m2) is True
    assert get_ml_problem(prob_id)["current_model_id"] == m2
    assert get_model(m2)["status"] == "production"
    assert get_model(m1)["status"] == "archived"

    # Wrong model id should raise
    bad_id = str(uuid.uuid4())
    with pytest.raises(ValueError):
        set_model_to_production(prob_id, bad_id)


# ---------------------------------------------------------
# 4) Delete helpers (manual cascades)
# ---------------------------------------------------------
def test_smoke_delete_helpers_and_cascades():
    _print_test("Delete helpers (manual cascades)")

    user_id = create_user("del_user", "del@example.com")
    ds_id = create_dataset("del_dataset", owner_id=user_id)
    dv_id = create_dataset_version(ds_id, uri="/data/del.csv", name="del_v1", filename="del.csv", schema_json={}, profile_json={}, row_count=1)
    prob_id = create_ml_problem(dataset_version_id=dv_id, task="classification", target="y", name="del_p1", dataset_version_uri="/data/del.csv")
    model_id, _ = create_model(problem_id=prob_id, name="del_m1", algorithm="algo", status="staging", created_by=user_id)
    job_id = create_job(job_type="train", problem_id=prob_id, model_id=model_id, status="queued", task_id="t1", requested_by=user_id)
    pred_id = create_prediction(name="del_pred1", model_id=model_id, input_uri="/in.json", inputs_json={}, outputs_json={}, outputs_uri="/out.json", status="completed", requested_by=user_id)

    # Single deletes
    assert delete_prediction(pred_id) is True
    assert get_prediction(pred_id) is None

    assert delete_job(job_id) is True
    assert get_job(job_id) is None

    # Recreate for cascade tests
    pred_id = create_prediction(name="del_pred2", model_id=model_id, input_uri="/in2.json", inputs_json={}, outputs_json={}, outputs_uri="/out2.json", status="completed", requested_by=user_id)
    job_id = create_job(job_type="train", problem_id=prob_id, model_id=model_id, status="queued", task_id="t2", requested_by=user_id)

    # delete_model should remove related predictions/jobs and clear current_model_id if set
    assert delete_model(model_id) is True
    assert get_model(model_id) is None
    assert get_prediction(pred_id) is None
    assert get_job(job_id) is None

    # Recreate model so we can delete problem/version/dataset
    model_id, _ = create_model(problem_id=prob_id, name="del_m2", algorithm="algo", status="staging", created_by=user_id)
    create_prediction(name="del_pred3", model_id=model_id, input_uri="/in3.json", inputs_json={}, outputs_json={}, outputs_uri="/out3.json", status="completed", requested_by=user_id)

    # delete_ml_problem should remove models (+ preds/jobs) and the problem row
    assert delete_ml_problem(prob_id) is True
    assert get_ml_problem(prob_id) is None
    assert get_model(model_id) is None

    # Recreate chain and test delete_dataset_version
    prob_id = create_ml_problem(dataset_version_id=dv_id, task="classification", target="y", name="del_p2", dataset_version_uri="/data/del.csv")
    model_id, _ = create_model(problem_id=prob_id, name="del_m3", algorithm="algo", status="staging", created_by=user_id)
    create_prediction(name="del_pred4", model_id=model_id, input_uri="/in4.json", inputs_json={}, outputs_json={}, outputs_uri="/out4.json", status="completed", requested_by=user_id)

    assert delete_dataset_version(dv_id) is True
    assert db_get_dataset_version(dv_id) is None
    assert get_ml_problem(prob_id) is None
    assert get_model(model_id) is None

    # Recreate version and test delete_dataset (full cascade)
    dv_id = create_dataset_version(ds_id, uri="/data/del2.csv", name="del_v2", filename="del2.csv", schema_json={}, profile_json={}, row_count=1)
    prob_id = create_ml_problem(dataset_version_id=dv_id, task="classification", target="y", name="del_p3", dataset_version_uri="/data/del2.csv")
    model_id, _ = create_model(problem_id=prob_id, name="del_m4", algorithm="algo", status="staging", created_by=user_id)
    create_prediction(name="del_pred5", model_id=model_id, input_uri="/in5.json", inputs_json={}, outputs_json={}, outputs_uri="/out5.json", status="completed", requested_by=user_id)

    assert delete_dataset(ds_id) is True
    assert db_get_dataset(ds_id) is None

    # After delete_dataset, everything downstream should be gone.
    stats = get_dashboard_stats()
    assert stats["datasets"] == 0
    assert stats["dataset_versions"] == 0
    assert stats["ml_problems"] == 0
    assert stats["models"] == 0
    assert stats["jobs"] == 0
    assert stats["predictions"] == 0


# ---------------------------------------------------------
# 5) Small edge cases (updates with no fields / wrong ids)
# ---------------------------------------------------------
def test_smoke_update_edge_cases():
    _print_test("Update edge cases")

    user_id = create_user("edge_user", "edge@example.com")
    ds_id = create_dataset("edge_dataset", owner_id=user_id)

    # Update with no fields should do nothing (returns False by design)
    assert update_dataset(ds_id, name=None, owner_id=None) is False

    # Non-existent id should return False
    assert update_dataset(str(uuid.uuid4()), name="nope") is False
