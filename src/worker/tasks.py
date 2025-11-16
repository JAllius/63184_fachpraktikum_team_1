import traceback
from time import sleep
from celery import states

# ! I don't know why. But. Celery decides to stop working when there is any relative import
# ! But ONLY if Celery itself starts the python code ¯\_(ツ)_/¯

import os
from celery import Celery


CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redis_server:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redis_server:6379")

celery_app = Celery(
    "celery",
    backend=CELERY_BROKER_URL,
    broker=CELERY_RESULT_BACKEND,
)


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
