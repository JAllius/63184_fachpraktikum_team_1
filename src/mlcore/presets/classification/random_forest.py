from typing import Literal, Tuple
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

VERSION = "1.0"

PRESETS = {
    "n_estimators":{
        "fast": 200,
        "balanced": 500,
        "accurate": 1000,
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
        "problem_id": "",
        "model_id": "",
        "model_uri": "",
        "task": "classification",
        "target": "",
        "preset": "random_forest",
        "version": VERSION,
        "framework": "scikit-learn",
        "algorithm": "RandomForestClassifier",
        "semantic_types": {
            "categorical": categorical,
            "numeric": numeric,
            "boolean": boolean,
            },
        "train_mode": train_mode,
        "schema_snapshot": {
            "X": {},
            "y": {},
            },
        "random_seed": random_seed,
        "metrics": {},
        "explanation": {},
        }
    
    
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", Pipeline([
                ("impute", SimpleImputer(strategy = "constant", fill_value = "__missing__")),
                ("ohe", OneHotEncoder(handle_unknown="ignore")),
                ]), categorical),
            ("num", Pipeline([
                ("impute", SimpleImputer(strategy = "median")),
                ("pass", "passthrough"),
                ]), numeric),
            ("bool", Pipeline([
                ("impute", SimpleImputer(strategy = "most_frequent")),
                ("pass", "passthrough"),
            ]), boolean)
        ]
    )
    
    params = {
        "n_estimators": PRESETS["n_estimators"][train_mode],
        "n_jobs": -1,
        "random_state": random_seed,
    }
    metadata["params"] = params
    
    rf = Pipeline([
        ("pre", preprocessor),
        ("est", RandomForestClassifier(**params)),
    ])
    
    return rf, metadata

def _bool_to_int(X):
    return X.astype(int)