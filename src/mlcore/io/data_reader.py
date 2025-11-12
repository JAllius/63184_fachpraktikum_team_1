import pandas as pd
from typing import Tuple


def get_dataframe(
    uri: str,
) -> pd.DataFrame:
    df = pd.read_csv(uri)
    return df

def _check_profile(profile):
    if not profile:
        raise ValueError("This dataset_version is missing a profile.")

def preprocess_dataframe(
    df: pd.DataFrame,
    target: str,
    profile: dict, 
    feature_strategy: dict | str = "auto",  
)-> Tuple[pd.DataFrame, pd.Series]:
    
    if feature_strategy == "auto":
        include = df.columns
        _check_profile(profile)
        exclude = profile["exclude_suggestions"]
    else:
        if feature_strategy.get("include", False):
            include = feature_strategy.get("include")
        else:
            include = df.columns
        if feature_strategy.get("exclude", False):
            exclude = feature_strategy.get("exclude")
            if target in exclude:
                raise ValueError(f"Target column '{target}' is in the exclusion list.")
        else:
            _check_profile(profile)
            exclude = profile["exclude_suggestions"]
    
    pre_cols = [column for column in df.columns if column in include and column not in exclude]
    df_pre = df[pre_cols]
    
    if target not in df_pre.columns:
        raise ValueError(f"Target column '{target}' not found in dataframe.")
    
    df_pre_notna = df_pre[df_pre["target"].notna() & (df_pre["target"] != "")]
    
    if not df_pre_notna[target].count():
        raise ValueError(f"Target column '{target}' is empty.")
    
    y = df_pre_notna[target]
    X = df_pre_notna.drop(columns= target)
    
    return X, y

def get_semantic_types(
    columns: list,
    profile: dict,
)-> dict:
    semantic_types = {
        "categorical": [],
        "numeric": [],
        "boolean": [],
    }
    
    _check_profile(profile)
    
    for column in columns:
        semantic_type = profile["columns"].get(column, {}).get("semantic_type")
        if semantic_type in semantic_types:
            semantic_types[semantic_type].append(column)

    return semantic_types
