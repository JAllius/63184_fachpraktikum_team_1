from typing import Any
import pandas as pd
from pathlib import Path
from mlcore.io.data_reader import get_dataframe_from_csv
from mlcore.io.model_loader import load_model
from mlcore.io.metadata_loader import load_metadata
from db.db import get_ml_problem, get_model, create_prediction
import numpy as np

def predict(
    input_df: pd.DataFrame | None = None,
    input_uri: str | None = None,
    problem_id: str | None = None,
    model_id: str | None = "production",
) -> tuple[pd.DataFrame, Any, dict]:

    if input_df is None and not input_uri:
        raise ValueError(
            "No input dataframe was specified. Provide an input or an input_uri.")

    if model_id == "production" and not problem_id:
        raise ValueError(
            "Not specified which model to load. Provide a problem_id or a model_id.")

    if input_uri:
        X = get_dataframe_from_csv(input_uri)
    else:
        X = input_df
    if X is None:
        raise ValueError("Input resolved to None.")

    if model_id == "production":
        problem = get_ml_problem(problem_id)
        if not problem.get("current_model_id"):
            raise ValueError("No production model set for this problem.")
        model_id = problem.get("current_model_id")
        model_db = get_model(model_id)
        if not model_db or not model_db.get("uri"):
            raise ValueError(f"Model '{model_id}' not found or has no uri.")
        model_path = Path(model_db.get("uri"))
        model = load_model(model_uri=model_path)
        metadata_path = model_path.with_name("metadata.json")
        metadata = load_metadata(metadata_path)
        target = metadata.get("target")
    else:
        model_db = get_model(model_id)
        model_path = Path(model_db.get("uri", False))
        model = load_model(model_uri=model_path)
        metadata_path = model_path.with_name("metadata.json")
        metadata = load_metadata(metadata_path)
        target = metadata.get("target")

    if target in X.columns:
        X = X.drop(columns=[target])

    schema_snapshot = metadata["schema_snapshot"]

    ### MISSING ###
    # Check schema snapshot and compare with X
    ### END MISSING ###

    y_pred = model.predict(X)

    label_classes = metadata.get("label_classes", None)
    if label_classes is not None:
        classes = np.array(label_classes, dtype=object) # dtype=object is not "needed", it is just for safety
        y_pred = classes[y_pred]

    prediction_summary = {
        "X": X.to_dict(orient="records"),
        "y_pred": y_pred.tolist() if hasattr(y_pred, "tolist") else list(y_pred),
        "model_metadata": metadata,
    }

    if input_df is None:
        inputs_to_store = None
    else:
        inputs_to_store = input_df.to_dict(orient="records")
    create_prediction(model_id, input_uri, inputs_to_store, prediction_summary, None, None)

    return X, y_pred, prediction_summary
