from ..celery_handler import celery_app
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import starlette.status as status
from typing import Literal, Optional
import logging
import json
import time
import os
from ..db.init_db import main
from ..db.db import create_dataset, db_get_dataset, db_get_dataset_version, get_datasets, get_dataset_versions, get_ml_problem, get_ml_problems, get_model, get_models, get_prediction, get_predictions

logger = logging.getLogger(__name__)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_domain(request: Request):
    """Takes a request and returns the domain as a string"""
    scheme = request.url.scheme  # "http" or "https"
    hostname = request.url.hostname  # "localhost" or "example.com"
    port = request.url.port  # e.g., 8000

    # Default ports for schemes
    default_ports = {"http": 80, "https": 443}
    domain = f"{scheme}://{hostname}"

    # Add port if non-default
    if port != default_ports.get(scheme):
        domain += f":{port}"
    return domain


# .on_event is deprecated and it suggests to use lifespan, but i don't know it. It should still support .on_event.
@app.on_event("startup")
def on_startup():
    duration = int(os.getenv("DELAY_DB_CONN_ON_STARTUP", 0))
    if duration > 0:
        logger.warning(
            f"Waiting for {duration}s for MySQL to finish startup")
        time.sleep(duration)
    main(apply_seed=False)

    seed_test_data = os.getenv("SEED_TEST_DATA", False).lower() == "true"
    if seed_test_data:
        test_data_path = os.getenv("TEST_DATA_PATH", "db/test_db.txt")
        try:
            from ..db.init_test_db import seed_db
            seed_db(test_data_path, reset=True)
        except Exception as e:
            print("Failed to seed the DB. Error: ", e)


@app.get("/")
async def read_root():
    logger.info("Sending celery task 'hello.task'")
    task = celery_app.send_task("hello.task", args=["world"])
    # return task id and url
    return RedirectResponse(url=f"/celery/{task.id}", status_code=status.HTTP_303_SEE_OTHER)


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
async def post_dataset(name: str,): # user_id: int):
    """create a stub for a new dataset and return the id"""
    dataset_id = create_dataset(name)
    return {dataset_id}


@app.get("/datasets")  # /datasets
async def get_list_datasets(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at"),
    dir: Literal["asc", "desc"] = Query("desc"),
    q: Optional[str] = Query(None),
    id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
):
    """get all datasets"""
    items, total = get_datasets(
        page=page,
        size=size,
        sort=sort,
        dir=dir,
        q=q,
        id=id,
        name=name,
    )
    total_pages = int((total + size -1)/size) if size > 0 else 1

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages,
        "sort": sort,
        "dir": dir,
        "q": q,
        "id": id,
        "name": name,
    }


@app.get("/dataset/{dataset_id}")
async def get_dataset(dataset_id: str): #, user_id: int):
    """return the specified dataset if user has permission"""
    dataset = db_get_dataset(dataset_id)
    return dataset


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


@app.get("/datasetVersion/{version}")
async def get_dataset_version(version: str): #, user_id: int):
    """return the specified dataset version if user has permission"""
    dataset_version = db_get_dataset_version(version)
    return dataset_version


@app.put("/dataset/{dataset_id}/{version}")
async def put_dataset_version(dataset_id: int, user_id: int):
    """update the specified dataset version if user has permission"""
    return {}


@app.delete("/dataset/{dataset_id}/{version}")
async def delete_dataset_version(dataset_id: int, user_id: int):
    """delete the specified dataset version if user has permission"""
    return {}


@app.get("/datasetVersions/{dataset_id}")  # /dataset_versions
async def get_list_dataset_versions(
    dataset_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at"),
    dir: Literal["asc", "desc"] = Query("desc"),
    q: Optional[str] = Query(None),
    id: Optional[str] = Query(None),
    #name: Optional[str] = Query(None),
):
    """get all dataset_versions"""
    items, total = get_dataset_versions(
        dataset_id=dataset_id,
        page=page,
        size=size,
        sort=sort,
        dir=dir,
        q=q,
        id=id,
        # name=name,
    )
    total_pages = int((total + size -1)/size) if size > 0 else 1

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages,
        "sort": sort,
        "dir": dir,
        "q": q,
        "id": id,
        # "name": name,
    }


@app.get("/datasetVersionProblems/{dataset_version_id}")  # ml_problems
async def get_list_problems(
    dataset_version_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at"),
    dir: Literal["asc", "desc"] = Query("desc"),
    q: Optional[str] = Query(None),
    id: Optional[str] = Query(None),
    task: Optional[str] = Query(None),
    target: Optional[str] = Query(None),
    #name: Optional[str] = Query(None),):   
):
    """get all ml_problems"""
    items, total = get_ml_problems(
        dataset_version_id=dataset_version_id,
        page=page,
        size=size,
        sort=sort,
        dir=dir,
        q=q,
        id=id,
        task=task,
        target=target,
        # name=name,
    )
    total_pages = int((total + size -1)/size) if size > 0 else 1

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages,
        "sort": sort,
        "dir": dir,
        "q": q,
        "id": id,
        "task": task,
        "target": target,
        # "name": name,
    }


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


@app.post("/problem")  # or ml_problems for clarity
async def post_problem(
    user_id: int,
    dataset_id: str,  # maybe we should concider having dataset_name UNIQUE in db so that we can replace this here with dataset_name
    target: str,
    task: Literal["classification", "regression"],
    dataset_version_id: int | str = "latest",
    # we will see later how we will impliment this exactly
    feature_strategy: dict | str = "auto",
    validation_strategy: Literal["CV", "holdout"] = "CV",  # for now only CV
):  # maybe later we will also add "anomaly_detection" and "timeseries"
    """create a new ml_problem and return problem_id"""
    return {}


@app.get("/problem/{problem_id}")
async def get_problem(problem_id: str):
    """return specified problem if user has permission"""
    ml_problem = get_ml_problem(problem_id)
    return ml_problem

# ========== ML_Train ==========


@app.post("/train")
async def post_train(
    # user_id: int,
    name: str,
    problem_id: str,
    algorithm: str = "auto",
    train_mode: Literal["fast", "balanced", "accurate"] = "balanced",
    evaluation_strategy: Literal["cv", "holdout"] = "cv",
    explanation: bool = True,
):
    """create a request/job to train a model for a given problem_id and return model_id"""
    logger.info("Sending celery task 'train.task'")

    # TODO: re-add user_id when we add checking for permissions
    task = celery_app.send_task(
        "train.task", args=[name, problem_id, algorithm, train_mode, evaluation_strategy, explanation])
    return RedirectResponse(url=f"/celery/{task.id}", status_code=status.HTTP_303_SEE_OTHER)

# ========== ML_Predict ==========


@app.post("/predict")
async def post_predict(
    input_json: str | None = None,
    input_uri: str | None = None,
    problem_id: str | None = None,
    model_id: str = "production",
):
    if model_id=="production" and not problem_id:
        # no problem or model given for the prediction
        raise HTTPException(status_code=400, detail="problem_id is required when model_id is not defined")
    if not input_json and not input_uri:
        # no input given for the prediction
        raise HTTPException(status_code=400, detail="Provide input or input_uri")
    """create a request/job to predict given a model and an input for a given problem_id and return prediction: json | str"""
    logger.info("Sending celery task 'predict.task'")

    task = celery_app.send_task(
        "predict.task", args=[input_json, input_uri, problem_id, model_id])
    return {"task_id": task.id, "status": f"/celery/{task.id}"}
    # return RedirectResponse(url=f"/celery/{task.id}", status_code=status.HTTP_303_SEE_OTHER)


# ========== ML_Models ==========


@app.get("/problemModels/{problem_id}")  # models
async def get_list_models(
    problem_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at"),
    dir: Literal["asc", "desc"] = Query("desc"),
    q: Optional[str] = Query(None),
    id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    algorithm: Optional[str] = Query(None),
    train_mode: Optional[str] = Query(None),
    evaluation_strategy: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """get all models"""
    items, total = get_models(
        problem_id=problem_id,
        page=page,
        size=size,
        sort=sort,
        dir=dir,
        q=q,
        id=id,
        name=name,
        algorithm=algorithm,
        train_mode=train_mode,
        evaluation_strategy=evaluation_strategy,
        status=status,
    )
    total_pages = int((total + size -1)/size) if size > 0 else 1

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages,
        "sort": sort,
        "dir": dir,
        "q": q,
        "id": id,
        "name":name,
        "algorithm":algorithm,
        "train_mode":train_mode,
        "evaluation_strategy":evaluation_strategy,
        "status":status,
    }


@app.get("/model/{model_id}")
async def get_model_info(model_id: str): #, user_id: int):
    """return the specified model if user has permission"""
    model = get_model(model_id)
    return model


# ========== ML_Predictions ==========


@app.get("/modelPredictions/{model_id}")  # models
async def get_list_predictions(
    model_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at"),
    dir: Literal["asc", "desc"] = Query("desc"),
    q: Optional[str] = Query(None),
    id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
):
    """get all predictions"""
    items, total = get_predictions(
        model_id=model_id,
        page=page,
        size=size,
        sort=sort,
        dir=dir,
        q=q,
        id=id,
        name=name,
    )
    total_pages = int((total + size -1)/size) if size > 0 else 1

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": total_pages,
        "sort": sort,
        "dir": dir,
        "q": q,
        "id": id,
        "name":name,
    }


@app.get("/prediction/{prediction_id}")
async def get_prediction_info(prediction_id: str): #, user_id: int):
    """return the specified model if user has permission"""
    prediction = get_prediction(prediction_id)
    return prediction


# I am not sure how this works with the storage and if we need an endpoint.
# get model (probably by id) -> return joblib object.
# For now we will have it locally (./testdata/models/{model_id}).
