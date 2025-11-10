from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"msg": "Hello World"}

# ========== Dataset ==========

@app.post("/dataset")  # /dataset?name=test&user_id=1
async def post_dataset(name:str, user_id: int):
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


