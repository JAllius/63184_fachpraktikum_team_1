# add project root to path for celery to work inside Docker
import sys  # nopep8
import os  # nopep8
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # nopep8

from celery_handler import celery_app
from mlcore.profile.profiler import suggest_profile
from mlcore.predict.predictor import predict
from mlcore.train.trainer import train
from celery import states
import traceback
from time import sleep
import pandas as pd


@celery_app.task(name="hello.task", bind=True)
def hello_world(self, name):
    try:
        # if name is error
        if name == "error":
            # will raise ZeroDivisionError
            a, b = 1, 0
            a = a / b

        # update task state every 1 second
        for i in range(10):
            sleep(1)
            self.update_state(state="PROGRESS", meta={"done": i, "total": 10})

        # return result
        return {"result": f"hello {name}"}

    # if any error occurs
    except Exception as ex:
        # update task state to failure
        self.update_state(
            state=states.FAILURE,
            meta={
                "exc_type": type(ex).__name__,
                "exc_message": traceback.format_exc().split("\n"),
            },
        )

        # raise exception
        raise ex


@celery_app.task(name="train.task", bind=True)
def train_task(
    self,
    problem_id: str,
    algorithm: str = "auto",
    train_mode: str = "balanced",
    explain: bool = True,
    test_size_ratio: float = 0.2,
    random_seed: int = 42,
):
    """
    Celery wrapper around mlcore.train.
    This is what FastAPI will call asynchronously for train.
    """
    try:
        self.update_state(state="STARTED", meta={"problem_id": problem_id})

        # Call core training logic
        model_uri = train(
            problem_id=problem_id,
            algorithm=algorithm,
            train_mode=train_mode,
            explain=explain,
            test_size_ratio=test_size_ratio,
            random_seed=random_seed,
        )

        # IF DB jobs table added -> update job status here
        return {"model_uri": model_uri}

    except Exception as ex:
        # update Celery state and meta to FAILURE
        self.update_state(
            state=states.FAILURE,
            meta={
                "exc_type": type(ex).__name__,
                "exc_message": traceback.format_exc().split("\n"),
            },
        )
        # IF DB jobs table added -> update job status here
        raise

# @celery_app.task(name="predict.task", bind=True)
# def predict_task(
#     self,
#     input: pd.DataFrame | dict | None = None,
#     input_uri: str | None = None,
#     problem_id: str | None = None,
#     model_uri: str | None = None,
#     model_id: str = "production",
# ):
#     """
#     Celery wrapper around mlcore.predict.
#     """
#     try:
#         self.update_state(state="STARTED", meta={"problem_id": problem_id})

#         # Rebuild DataFrame ONLY if input is a dict
#         if input is not None:
#             if isinstance(input, dict):
#                 input = pd.DataFrame(input)

#         X, y_pred, summary = predict(
#             input=input,
#             input_uri=input_uri,
#             problem_id=problem_id,
#             model_uri=model_uri,
#             model_id=model_id,
#         )

#         return {
#             "y_pred": summary["y_pred"].tolist(),
#             "n_predictions": summary["n_predictions"],
#             "model_metadata": summary["model_metadata"],
#         }

#     except Exception as ex:
#         self.update_state(
#             state=states.FAILURE,
#             meta={
#                 "exc_type": type(ex).__name__,
#                 "exc_message": traceback.format_exc().split("\n"),
#             },
#         )
#         raise


# @celery_app.task(name="profile.task", bind=True)
# def suggest_profile_task(self, df_dict: dict | pd.DataFrame):
#     """
#     Celery wrapper for suggest_profile(df).
#     df_dict = DataFrame serialized as dict-of-lists
#     """
#     try:
#         self.update_state(state="STARTED")

#         if isinstance(df, dict):
#             df = pd.DataFrame(df)

#         profile = suggest_profile(df)

#         return profile

#     except Exception as ex:
#         self.update_state(
#             state=states.FAILURE,
#             meta={
#                 "exc_type": type(ex).__name__,
#                 "exc_message": traceback.format_exc().split("\n"),
#             },
#         )
#         raise
