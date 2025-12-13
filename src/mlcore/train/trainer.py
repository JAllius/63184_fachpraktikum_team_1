from mlcore.io.preset_loader import loader
from mlcore.io.data_reader import get_dataframe_from_csv, preprocess_dataframe, get_semantic_types
from mlcore.io.model_saver import save_model
from mlcore.io.metadata_saver import save_metadata
from mlcore.profile.profiler import suggest_profile
from mlcore.explain.explanator import explain_model
from mlcore.metrics.metrics_calculator import calculate_metrics
from mlcore.metrics.cv_calculator import calculate_cv
from sklearn.model_selection import train_test_split
from typing import Literal, Tuple
import pandas as pd
from db.db import db_get_dataset_version, get_ml_problem, create_model
import json
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

BASE_DIR = "./testdata/models"
PRESET_DIR = "/code/mlcore/presets"
NAME = None

def train(
    problem_id: str,
    algorithm: str = "auto",
    train_mode: Literal["fast", "balanced", "accurate"] = "balanced",
    evaluation_strategy: Literal["cv", "holdout"] = "cv",
    explain: bool = True,
    test_size_ratio: float = 0.2,
    random_seed: int = 42,
    preset_dir: str = PRESET_DIR,
) -> Tuple[str, str]:

    problem = get_ml_problem(problem_id)
    dataset_version_id = problem.get("dataset_version_id", False)
    target = problem.get("target", False)
    dataset_version = db_get_dataset_version(dataset_version_id)

    df = get_dataframe_from_csv(
        dataset_version.get("uri", False))
    raw_profile = dataset_version.get("profile_json")
    profile = json.loads(raw_profile) if isinstance(
        raw_profile, str) else raw_profile
    if not profile:
        profile = suggest_profile(pd.DataFrame(df))
    multi_class = profile.get("columns", {}).get(
        target, {}).get("cardinality", 0) > 2

    X, y = preprocess_dataframe(df, target, profile)
    semantic_types = get_semantic_types(X, profile)
    task = problem.get("task")

    categorical = semantic_types["categorical"]
    numeric = semantic_types["numeric"]
    boolean = semantic_types["boolean"]

    X_train, X_test, y_train, y_test = train_test_split(
        # stratify to keep class proportions
        X, y, test_size=test_size_ratio, stratify=y, random_state=random_seed
    )

    build_model = loader(task, algorithm.lower(), preset_dir)

    model, metadata = build_model(categorical, numeric, boolean, train_mode)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = calculate_metrics(y_test, y_pred, task, multi_class)
    if evaluation_strategy == "cv":
        cv = calculate_cv(model, X_train, y_train, task, multi_class)
        metadata["cross_validation"] = cv

    explanation = {}
    if explain:
        model_shap = model.named_steps.get("est")
        preprocessor = model.named_steps.get("pre")
        X_train_shap = preprocessor.transform(X_train)
        X_test_shap = preprocessor.transform(X_test)
        # explanation = explain_model(task, model_shap, X_train_shap, X_test_shap)
        explain_model(task, model_shap, X_train_shap, X_test_shap)

    metadata["problem_id"] = problem_id
    metadata["target"] = target
    metadata["schema_snapshot"]["X"] = {
        column: str(X[column].dtype) for column in X.columns
    }
    metadata["schema_snapshot"]["y"] = {
        y.name: str(y.dtype)
    }
    metadata["metrics"] = metrics
    if explanation:
        metadata["explanation"] = explanation

    model_id, model_uri = create_model(
        problem_id=problem_id,
        algorithm=algorithm.lower(),
        status="staging",
        train_mode=train_mode,
        evaluation_strategy=evaluation_strategy,
        metrics_json=metrics,
        uri=None,
        metadata_uri=None,
        explanation_uri=None,
        created_by=NAME,
        name=None,
    )

    metadata["model_id"] = model_id

    parent_path = Path(model_uri).parent

    if save_model(model, parent_path):
        logger.info(f"[SAVE_MODEL] Model saved at: {model_uri}")
        if save_metadata(metadata, parent_path):
            logger.info(f"[SAVE_MODEL_METADATA] Model's metadata saved at: {model_uri}")
            return model_id, model_uri
        else:
            logger.error(f"[SAVE_MODEL_METADATA] Failed to save model's metadata at: {model_uri}")
            raise RuntimeError(
                f"Failed to save the model's metadata at {parent_path}")
    else:
        logger.error(f"[SAVE_MODEL] Failed to save model at: {model_uri}")
        raise RuntimeError(f"Failed to save the model at {parent_path}")
