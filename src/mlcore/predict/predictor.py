from db.db import get_ml_problem
import pandas as pd


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

    # TODO: Check schema snapshot and compare with X
    # schema_snapshot = metadata["schema_snapshot"]

    y_pred = model.predict(X)

    prediction_summary = {
        "X": X.to_dict(orient="records"),
        "y_pred": y_pred.tolist() if hasattr(y_pred, "tolist") else list(y_pred),
        "model_metadata": metadata,
    }

    if input is None:
        inputs_to_store = None
    else:
        inputs_to_store = input.to_dict(orient="records")
    create_prediction(model_id, None, inputs_to_store,
                      prediction_summary, None, None)

    return X, y_pred, prediction_summary
