import pandas as pd


def get_dataframe(
    uri: str,
) -> pd.DataFrame:
    df = pd.read_csv(uri)
    return df
