from .profiler import suggest_profile, suggest_schema
from src.mlcore.io.data_reader import get_dataframe
import pandas as pd


def test_suggest_profile():
    df = get_dataframe("./testdata/profiler/test_dataset.csv")
    profile = suggest_profile(pd.DataFrame(df))
    assert isinstance(profile, dict)
