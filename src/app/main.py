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


