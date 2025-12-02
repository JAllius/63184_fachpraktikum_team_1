from typing import Literal, Tuple
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from autosklearn.classification import AutoSklearnClassifier
from ..metadata_presets import metadata_preset

VERSION = "1.0"

PRESETS = {
    "time_left_for_this_task":{
        "fast": 60,
        "balanced": 300,
        "accurate": 900,
    },
    "per_run_time_limit":{
        "fast": 15,
        "balanced": 60,
        "accurate": 90,
    },
}

def build_model(
    categorical: list = [],
    numeric: list = [],
    boolean: list = [],
    train_mode: Literal["fast", "balanced", "accurate"] = "balanced",
    random_seed: int = 42,
)-> Tuple[Pipeline, dict]:
    
    metadata = {
        **metadata_preset,  # merge metadata with the preset
        "task": "classification",
        "preset": "auto",
        "version": VERSION,
        "framework": "auto-sklearn",
        "algorithm": "AutoSklearnClassifier",
        "semantic_types": {
            "categorical": categorical,
            "numeric": numeric,
            "boolean": boolean,
            },
        "train_mode": train_mode,
        "random_seed": random_seed,
        }

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", Pipeline([
                ("impute", SimpleImputer(strategy = "constant", fill_value = "__missing__")),
                ("ohe", OneHotEncoder(handle_unknown="ignore")),
                ]), categorical),
            ("num", Pipeline([
                ("impute", SimpleImputer(strategy = "median")),
                ("scale", StandardScaler()),
                ]), numeric),
            ("bool", Pipeline([
                ("impute", SimpleImputer(strategy = "most_frequent")),
                ("pass", "passthrough"),
            ]), boolean)
        ]
    )
    
    params = {
        "time_left_for_this_task": PRESETS["time_left_for_this_task"][train_mode],
        "per_run_time_limit": PRESETS["per_run_time_limit"][train_mode],
        "n_jobs": -1,
        "seed": random_seed,
    }
    metadata["params"] = params
    
    model = Pipeline([
        ("pre", preprocessor),
        ("est", AutoSklearnClassifier(**params)),
    ])
    
    return model, metadata