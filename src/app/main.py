from ..celery_handler import celery_app
from fastapi import FastAPI
from typing import Literal
import logging
import json

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def read_root():
    task = celery_app.send_task("hello.task", args=["world"])
    # return task id and url
    return dict(
        id=task.id,
        url=f"localhost:42000/celery/{task.id}",
    )


@app.get("/celery/{id}")
def check_task(id: str):
    # get celery task from id
    task = celery_app.AsyncResult(id)

    # if task is in success state
    if task.state == "SUCCESS":
        response = {
            "status": task.state,
            "result": task.result,
            "task_id": id,
        }

    # if task is in failure state
    elif task.state == "FAILURE":
        response = json.loads(
            task.backend.get(
                task.backend.get_key_for_task(task.id),
            ).decode("utf-8")
        )
        del response["children"]
        del response["traceback"]

    # if task is in other state
    else:
        response = {
            "status": task.state,
            "result": task.info,
            "task_id": id,
        }

    # return response
    return response

# ========== Dataset ==========


@app.post("/dataset")  # /dataset?name=test&user_id=1
async def post_dataset(name: str, user_id: int):
    """create a stub for a new dataset and return the id"""
    return {}


@app.get("/dataset/{dataset_id}")
async def get_dataset(dataset_id: int, user_id: int):
    """return the specified dataset if user has permission"""
    return {}


@app.put("/dataset/{dataset_id}")
async def put_dataset(dataset_id: int, user_id: int):
    """update the specified dataset if user has permission"""
    return {}


@app.delete("/dataset/{dataset_id}")
async def delete_dataset(dataset_id: int, user_id: int):
    """delete the specified dataset if user has permission"""
    return {}

# ========== Dataset version ==========

# TODO: allow .csv upload on Write-Paths


@app.post("/dataset/{dataset_id}")
async def post_dataset_version(dataset_id: int, user_id: int):
    """create a stub for a new dataset version and return the version"""
    return {}


@app.get("/dataset/{dataset_id}/{version}")
async def get_dataset_version(dataset_id: int, version: int, user_id: int):
    """return the specified dataset version if user has permission"""
    return {}


@app.put("/dataset/{dataset_id}/{version}")
async def put_dataset_version(dataset_id: int, user_id: int):
    """update the specified dataset version if user has permission"""
    return {}


@app.delete("/dataset/{dataset_id}/{version}")
async def delete_dataset_version(dataset_id: int, user_id: int):
    """delete the specified dataset version if user has permission"""
    return {}

# ========== Profile specification ==========

# TODO: get known algorithms from database and check if specified algorithm is available

# ========== Jobs ==========

# TODO: CRUD for jobs (perform a task on a given dataset (version) with (autodetected) profile)


@app.post("/jobs")
async def post_job(dataset_id: int, version: int, profile: str, user_id: int):
    """create a new job and return job id"""
    return {}


@app.get("/jobs/{job_id}")
async def get_job(user_id: int):
    """return specified job if user has permission"""
    return {}

# TODO: can an existing job be updated? or only aborted (deleted)
# @app.put("/jobs/{job_id}")
# async def put_job(user_id: int):
#     """update specified job if user has permission"""
#     return {}


@app.delete("/jobs/{job_id}")
async def delete_job(user_id: int):
    """abort and delete specified job if user has permission"""
    return {}
# ========== ML_Problems ==========

 # TODO: later update/delete too but not so important for now.


@app.post("/problems")  # or ml_problems for clarity
async def post_problem(
    user_id: int,
    dataset_id: str,  # maybe we should concider having dataset_name UNIQUE in db so that we can replace this here with dataset_name
    target: str,
    dataset_version_id: int | str = "latest",
    task: Literal["classification", "regression", "auto"] = "auto",
    # we will see later how we will impliment this exactly
    feature_strategy: dict | str = "auto",
    validation_strategy: Literal["CV", "holdout"] = "CV",  # for now only CV
):  # maybe later we will also add "anomaly_detection" and "timeseries"
    """create a new ml_problem and return problem_id"""
    return {}


@app.get("/problems/{problem_id}")
async def get_problem(problem_id: int):
    """return specified problem if user has permission"""
    return {}

# ========== ML_Train ==========


@app.post("/train")
async def post_train(
    user_id: int,
    problem_id: int,
    algorithm: str = "auto",
    train_mode: Literal["fast", "balanced", "accurate"] = "balanced",
    explanation: bool = True,
):
    """create a request/job to train a model for a given problem_id and return model_id"""
    return {}

# ========== ML_Predict ==========


@app.post("/predict")
async def post_predict(
    user_id: int,
    problem_id: int | None = None,
    model_id: int | str = "production",
    input: str | None = None,
    input_uri: str | None = None,
    train_mode: Literal["fast", "balanced", "accurate"] = "balanced",
    explanation: bool = True,
):
    if not problem_id and model_id == "production":
        # no problem or model given for the prediction
        return {}
    if not input and not input_uri:
        # no input given for the prediction
        return {}
    """create a request/job to predict given a model and an input for a given problem_id and return prediction: json | str"""
    return {}

# ========== ML_Models ==========

# I am not sure how this works with the storage and if we need an endpoint.
# get model (probably by id) -> return joblib object.
# For now we will have it locally (./testdata/models/{model_id}).
