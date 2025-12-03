import pandas as pd
from pathlib import Path
from mlcore.io.data_reader import get_dataframe_from_csv
from mlcore.io.model_loader import load_model
from mlcore.io.metadata_loader import load_metadata
from db.db import get_ml_problem, get_model


def predict(
    input: pd.DataFrame | None = None,
    input_uri: str | None = None,
    problem_id: str | None = None,
    model_uri: str | None = None,
    model_id: str | None = "production",
) -> str:

    if not input and not input_uri:
        raise ValueError(
            "No input dataframe was specified. Provide an input or an input_uri.")

    if not model_uri and not problem_id:
        raise ValueError(
            "Not specified which model to load. Provide a problem_id or a model_uri.")

    if input_uri:
        X = get_dataframe_from_csv(input_uri)
    else:
        X = input

    if model_uri:
        model = load_model(model_uri=model_uri)
        model_path = Path(model_uri)
        metadata_path = model_path.with_name("metadata.json")
        metadata = load_metadata(metadata_path)
        target = metadata.get("target")
    else:
        if model_id == "production":

            problem = get_ml_problem(problem_id)
            model_id = problem.get("current_model_id", False)
            model = get_model(model_id)
            model_path = model.get("uri", False)

            model = load_model(model_uri=model_path)
            metadata_path = model_path.with_name("metadata.json")
            metadata = load_metadata(metadata_path)
            target = metadata.get("target")
        else:
            model = load_model(problem_id=problem_id, model_id=model_id)
            metadata = load_metadata(problem_id=problem_id, model_id=model_id)
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
