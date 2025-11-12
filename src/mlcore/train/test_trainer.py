from .trainer import classification
from src.mlcore.io.synthetic_generators import gen_classification
from numpy import ndarray
from src.mlcore.io.data_reader import get_dataframe, preprocess_dataframe, get_semantic_types
from src.mlcore.profile.profiler import suggest_profile
import pandas as pd

def test_gen_classification():
    X, y = gen_classification(5000, 3, 3, 42)
    assert isinstance(X, ndarray)
    assert isinstance(y, ndarray) 
    print(classification(X, y, 42))

def test_classification():
    X, y = gen_classification(5000, 3, 3, 42)
    out = classification(X, y, 42)
    assert isinstance(out, str)
    
def test_trainer():
    df = get_dataframe("./testdata/test_dataset.csv")
    profile = suggest_profile(pd.DataFrame(df))
    X, y = preprocess_dataframe(df, "target", profile)
    semantic_types = get_semantic_types(X, profile)
    report = classification(X, y, semantic_types)
    print(report)
    assert isinstance(profile, dict)