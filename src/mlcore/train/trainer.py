from ..io.preset_loader import loader
from ..io.data_reader import get_dataframe_from_csv, preprocess_dataframe, get_semantic_types
from ..io.model_saver import save_model
from ..profile.profiler import suggest_profile
from ..explain.explanator import explain_model
from ..metrics.calculator import calculate_metrics
from sklearn.model_selection import train_test_split
from typing import Literal
import pandas as pd
import json


def train(
    problem_id: str,
    algorithm: str = "auto",
    train_mode: Literal["fast", "balanced", "accurate"] = "balanced",
    explain: bool = True,
    test_size_ratio: float = 0.2,
    random_seed: int = 42,
) -> str:

    ### CHANGE WITH DB FUNCTION LATER ###
    with open("./testdata/ml_problems.json", "r") as f:
        problems = json.load(f)
    problem = problems[problem_id]
    with open("./testdata/dataset_versions.json", "r") as f:
        dataset_versions = json.load(f)
    dataset_version = dataset_versions[problem.get(
        "dataset_version_id", False)]
    ### END OF CHANGE ###

    df = get_dataframe_from_csv(
        dataset_version.get("dataset_version_uri", False))
    if not dataset_version.get("profile", False):
        profile = suggest_profile(pd.DataFrame(df))
    profile = dataset_version.get("profile", False)

    X, y = preprocess_dataframe(df, "target", profile)
    semantic_types = get_semantic_types(X, profile)
    task = problem.get("task")

    categorical = semantic_types["categorical"]
    numeric = semantic_types["numeric"]
    boolean = semantic_types["boolean"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size_ratio, stratify=y, random_state=random_seed
    )

    build_model = loader(task, algorithm)

    # Missing metadata handling - filling
    model, metadata = build_model(categorical, numeric, boolean, train_mode)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = calculate_metrics(y_test, y_pred, task)

    explanation = {}
    if explain:
        model_shap = model.named_steps.get("est")
        preprocessor = model.named_steps.get("pre")
        X_train_shap = preprocessor.transform(X_train)
        X_test_shap = preprocessor.transform(X_test)
        # explanation = explain_model(task, model_shap, X_train_shap, X_test_shap)
        explain_model(task, model_shap, X_train_shap, X_test_shap)

    # model_id = uuid.uuid4()
    model_id = "c5d6ecb2-4c62-4fcb-a85a-63f9e8d3e4b9"
    metadata["problem_id"] = problem_id
    metadata["model_id"] = model_id
    metadata["target"] = problem.get("target")
    metadata["schema_snapshot"]["X"] = {
        column: str(X[column].dtype) for column in X.columns
    }
    metadata["schema_snapshot"]["y"] = {
        y.name: str(y.dtype)
    }
    metadata["metrics"] = metrics
    if explanation:
        metadata["explanation"] = explanation

    model_uri = save_model(model, metadata, problem_id,
                           model_id, "./testdata/models")

    return model_uri
