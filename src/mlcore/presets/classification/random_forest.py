from typing import Literal, Tuple
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

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
    
    pre_tree = ColumnTransformer(
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
                ("to_int", FunctionTransformer(lambda X: X.astype(int))), # transform boolean dtypes to int 1/0
            ]), boolean)
        ]
    )
    rf = Pipeline([
        ("pre", pre_tree),
        ("clf", RandomForestClassifier(
            n_estimators = PRESETS["n_estimators"][train_mode],
            n_jobs = -1,
            random_state = random_seed,
        )),
    ])
    
    # Missing Metadata
    return rf, {}