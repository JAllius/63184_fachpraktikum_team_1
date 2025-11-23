from .db import (
    create_dataset, create_dataset_version, get_dataset,
    create_ml_problem, save_model_metadata,
    create_job, update_job_status,
    save_prediction, get_model, get_job, get_prediction,
)
import pytest
import os
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def init_db():
    from .init_db import main
    main(apply_seed=False)


@pytest.mark.skipif(os.environ.get("PYTEST_CI_MODE"), reason="does not work in CI pipeline")
def test_initialize_app_db(init_db):
    return


@pytest.mark.skipif(os.environ.get("PYTEST_CI_MODE"), reason="does not work in CI pipeline")
def test_db_smoke(init_db):
    ds_id = create_dataset("sales_store_1", "team1")
    ver_id = create_dataset_version(
        ds_id, "/data/sales_2025_01.csv",
        schema_json={"date": "DATE", "sales": "INT"},
        profile_json={"rows": 1000}, row_count=1000
    )
    prob_id = create_ml_problem(ver_id, "timeseries", "sales",
                                feature_strategy_json={"include": ["date"]},
                                validation_strategy="train_test_split")
    job_id = create_job("train", problem_id=prob_id)
    update_job_status(job_id, "running")
    model_id = save_model_metadata(prob_id, "prophet", "staging",
                                   metrics_json={"MAE": 123.4},
                                   model_uri="/models/prophet_store1_v1.joblib",
                                   name="prophet_store1_v1")
    update_job_status(job_id, "completed")
    pjob_id = create_job("predict", problem_id=prob_id, model_id=model_id)
    update_job_status(pjob_id, "running")
    pred_id = save_prediction(prob_id, model_id, pjob_id,
                              inputs_json={"date": "2025-01-31"},
                              outputs_json={"sales_pred": 987})
    update_job_status(pjob_id, "completed")

    logger.info("dataset:", get_dataset(ds_id))
    logger.info("model:", get_model(model_id))
    logger.info("prediction:", get_prediction(pred_id))


if __name__ == "__main__":
    test_db_smoke()
