import pandas as pd
from pathlib import Path
from mlcore.io.data_reader import get_dataframe_from_csv
from db.db import get_ml_problem, get_model, get_model_dump


def predict(
    input: pd.DataFrame,
    problem_id: str,
    model_id: str = "production",
) -> str:
    X = input

    if model_id == "production":
        # TODO: different behaviour for default value?
        problem = get_ml_problem(problem_id)
        model_id = problem.get("current_model_id", False)
        model = get_model(model_id)
        metadata = get_model_dump(model_id)["metadata_json"]
        target = metadata.get("target")
    else:
        model = get_model(model_id)
        metadata = get_model_dump(model_id)["metadata_json"]
        target = metadata.get("target")

    if target in X.columns:
        X = X.drop(columns=[target])

    schema_snapshot = metadata["schema_snapshot"]

    ### MISSING ###
    # Check schema snapshot and compare with X
    ### END MISSING ###

    y_pred = model.predict(X)

    prediction_summary = {
        "X": X,
        "y_pred": y_pred,
        "model_metadata": metadata,
    }

    return X, y_pred, prediction_summary
