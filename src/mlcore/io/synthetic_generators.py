from sklearn.datasets import make_classification, make_regression
import pandas as pd
import numpy as np

def gen_classification(n_samples, n_classes, n_informative, random_state):
    X, y = make_classification(n_samples= n_samples, n_classes= n_classes, n_informative= n_informative, random_state= random_state)
    return X, y

def gen_regression(n_samples, n_classes, random_state):
    x, y = make_regression(n_samples= n_samples, n_classes= n_classes, random_state= random_state)
    return x, y

def gen_csv(size: int = 20, random_seed: int = 42):
    np.random.seed(random_seed)
    df = pd.DataFrame({
        "id": range(1, size + 1),
        "age": np.random.randint(18, 70, size=size),
        "income": np.random.choice([40000, 55000, 70000, np.nan], size=size),
        "gender": np.random.choice(["Male", "Female", "Other", np.nan], size=size),
        "signup_date": pd.date_range("2024-01-01", periods=size, freq="ME"),
        "target": np.random.choice([0, 1], size=size),
        "notes": np.random.choice(["good", "bad", "average", np.nan], size=size),
        "mixed_col": np.random.choice(["5", "text", np.nan, "7.5"], size=size)
    })

    df.to_csv("test_dataset.csv", index=False)
    print("CSV saved as: test_dataset.csv")
    print(df.head())
    return df