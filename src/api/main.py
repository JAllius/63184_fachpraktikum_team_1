import shutil
from ..celery_handler import celery_app
from fastapi import FastAPI, File, Form, HTTPException, Request, Query, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import starlette.status as status
from typing import Literal, Optional
import logging
import json
import time
import os
from ..db.init_db import main
from ..db.db import create_dataset, create_dataset_version, create_ml_problem, db_get_dataset, db_get_dataset_version, get_dashboard_stats, get_datasets, get_dataset_versions, get_ml_problem, get_ml_problems, get_model, get_models, get_prediction, get_predictions
from ..mlcore.profile.profiler import suggest_profile, suggest_schema
from ..mlcore.io.data_reader import get_dataframe_from_csv, preprocess_dataframe, get_semantic_types
from pathlib import Path

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
    return dataset_id


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

UPLOAD_DIR = Path("/code/worker/testdata/")
def save_file(file: UploadFile):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file selected")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    filename = file.filename
    file_path = UPLOAD_DIR / filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return str(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

@app.post("/datasetVersion")
async def post_dataset_version(
    dataset_id: str = Form(...),
    name: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    file_id: Optional[str] = Form(None),): #, user_id: int):
    """create a stub for a new dataset version and return the version"""
    if not file and not file_id:
        return {}
    if file:
        uri = save_file(file)
        if not uri:
            return {}
    if file_id:
        return {}
    
    # TO BE ADDED TO TASK AND UPDATE WHEN READY
    df = get_dataframe_from_csv(uri)
    profile_json = suggest_profile(df)
    schema_json = suggest_schema(df)
    # END OF COMMENT
    
    dataset_version_id = create_dataset_version(dataset_id=dataset_id, uri=uri, name=name, schema_json=schema_json, profile_json=profile_json)
    return dataset_version_id


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

@app.post("/profile/{dataset_version_id}")
async def post_profile(dataset_version_id: str): #, user_id: int):
    """run the profile of dataset_version and save to the database"""
    return {}

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
    # user_id: int,
    # dataset_id: str,  # maybe we should concider having dataset_name UNIQUE in db so that we can replace this here with dataset_name
    target: str,
    task: Literal["classification", "regression"],
    dataset_version_id: int | str = "latest",
    name: str | None = None,
):  # maybe later we will also add "anomaly_detection" and "timeseries"
    """create a new ml_problem and return problem_id"""
    # TO BE ADDED TO TASK AND UPDATE WHEN READY
    dataset_version = await get_dataset_version(dataset_version_id)
    raw_profile = dataset_version.get("profile_json")
    profile = json.loads(raw_profile) if isinstance(raw_profile, str) and raw_profile else {}
    uri = dataset_version.get("uri")
    if not uri:
        raise HTTPException(status_code=400, detail="Dataset version has no URI")
    df = get_dataframe_from_csv(uri)
    X, y = preprocess_dataframe(df, target, profile)
    semantic_types = get_semantic_types(X, profile)
    # END OF COMMENT
    ml_problem_id = create_ml_problem(target=target, task=task, dataset_version_id=dataset_version_id, name=name, semantic_types=semantic_types)
    return ml_problem_id


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


# ========== Dashboard Stats ==========


@app.get("/dashboard/stats")
async def get_dashboard_stats_info(): #, user_id: int):
    """return the dashboard stats if user has permission"""
    stats = get_dashboard_stats()
    return stats


# ========== Presets ==========

def list_presets(task: Literal["classification", "regression"], base_dir: str = "/code/mlcore/presets") -> list[str]:
    task_dir = os.path.join(base_dir, task)
    if not os.path.isdir(task_dir):
        raise ValueError(
            f"Failed to find a directory for this task {task}.")
    
    presets = set()
    
    for file in os.listdir(task_dir):
        # read only python files
        if not file.endswith(".py"):
            continue
        # skip private / init files
        if file == "__init__.py" or file.startswith("_"):
            continue
        preset_name = os.path.splitext(file)[0]
        presets.add(preset_name)
    
    return sorted(presets)

@app.get("/presets/{task}")
async def get_presets_list(task): #, user_id: int):
    """return the preset_list"""
    presets = list_presets(task)
    return presets