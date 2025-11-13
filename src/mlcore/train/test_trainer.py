from .trainer import train
from ..io.data_reader import get_dataframe_from_csv, preprocess_dataframe, get_semantic_types
from ..profile.profiler import suggest_profile
import pandas as pd


def test_trainer():
    df = get_dataframe_from_csv("./testdata/test_dataset.csv")
    profile = suggest_profile(pd.DataFrame(df))
    X, y = preprocess_dataframe(df, "target", profile)
    semantic_types = get_semantic_types(X, profile)
    report = train("classification", X, y,
                   semantic_types, "random_forest")
    print(report)
    assert isinstance(profile, dict)
