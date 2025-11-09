import pandas as pd
import pandas.api.types as pdtypes
import numpy as np
from src.mlcore.io.synthetic_generators import gen_classification
from src.mlcore.io.synthetic_generators import gen_csv
from src.mlcore.io.data_reader import get_dataframe

def suggest_schema(
    df: pd.DataFrame
)-> dict:
    schema = {}
    for column in df.columns:
        schema[column] = str(df[column].dtype)
    return schema

def _analyse_column(column: pd.Series)-> dict:
    column_summary = {}
    unique_count = column.nunique(dropna=True)
    non_zero_count = column.count()
    missing_pct = round(float(1 - non_zero_count/len(column)), 4)
    column_summary["missing_pct"] = missing_pct
    column_summary["dtype_raw"] = str(column.dtype)
        
    if non_zero_count == 0:
        column_summary["semantic_type"] = "unstructured"
        column_summary["cardinality_ratio"] = 0.0
        column_summary["suggested_analysis"] = ""
        column_summary["exclude_for_analysis"] = True
        column_summary["is_empty"] = True
        column_summary["is_constant"] = True
        column_summary["is_unique"] = False
        # return column_summary, is_id_candidate (= False)
        return column_summary, False
        
    # Cardinality_ratio is calculated as (unique non-NaN values)/(total non-NaN values).    
    cardinality_ratio = round(float(unique_count/non_zero_count), 4)
        
    if pdtypes.is_bool_dtype(column):
        column_summary["semantic_type"] = "boolean"
        column_summary["cardinality_ratio"] = cardinality_ratio
        column_summary["suggested_analysis"] = "classification"
        column_summary["exclude_for_analysis"] = False
    if pdtypes.is_integer_dtype(column):
        column_summary["semantic_type"] = "numerical"
        column_summary["cardinality_ratio"] = cardinality_ratio
        # For integers check cardinality ratio to suggest analysis type.
        # If the cardinality ratio is low <= 20%, suggest classification.
        # If the cardinality ratio is high > 20%, suggest regression.
        if cardinality_ratio <= 0.2:
            column_summary["suggested_analysis"] = "classification"
        else:
            column_summary["suggested_analysis"] = "regression"
        column_summary["exclude_for_analysis"] = False
    if pdtypes.is_float_dtype(column):
        column_summary["semantic_type"] = "numerical"
        column_summary["cardinality_ratio"] = cardinality_ratio
        column_summary["suggested_analysis"] = "regression"
        column_summary["exclude_for_analysis"] = False
    if pdtypes.is_datetime64_any_dtype(column):
        column_summary["semantic_type"] = "datetime"
        column_summary["cardinality_ratio"] = cardinality_ratio
        column_summary["suggested_analysis"] = ""
        # Datetimes are in general not useful for ML analysis (timestamps, etc), suggest to drop for analysis.
        column_summary["exclude_for_analysis"] = True
    if column.dtype == "object":
        # For objects: check cardinality to understand if it is a categorical column or not.
        # 3-rule check:
        #   1) If the cardinality is low <= 20, suggest categorical semantic type. (could be changed to 10 for stricter results)
        #   2) If the cardinality ratio is low <= 20%, suggest categorical semantic type.
        #   3) If the frequencies of the top 3 categories cover more than 80% of the non-NaN values, suggest categorical semantic type.
        # If all the checks fail, suggest unstructured semantic type and to drop for analysis.
        if cardinality_ratio <= 0.2:
            column_summary["semantic_type"] = "categorical"
            column_summary["cardinality_ratio"] = cardinality_ratio
            column_summary["suggested_analysis"] = "classification"
            column_summary["exclude_for_analysis"] = False
        else:
            column_summary["semantic_type"] = "unstructured"
            column_summary["cardinality_ratio"] = cardinality_ratio
            column_summary["suggested_analysis"] = ""
            column_summary["exclude_for_analysis"] = True
    
    column_summary["is_empty"] = False
    column_summary["is_constant"] = unique_count < 2
    column_summary["is_unique"] = cardinality_ratio == 1.0
    # if column_summary["semantic_type"] == "categorical" and cardinality_ratio == 1.0:
    #     column_summary["exclude_for_analysis"] = True
    
    return column_summary

def suggest_profile(
    df: pd.DataFrame
)-> dict:
    profile = {}
    n_rows, n_cols = df.shape
    non_zero_count = sum(df.count(0))
    missing_pct = round(1 - non_zero_count/(n_cols*n_rows), 4)
    summary = {}
    summary["n_rows"] = n_rows
    summary["n_cols"] = n_cols
    summary["missing_pct"] = missing_pct
    profile["summary"] = summary
    profile["id_candidates"] = []
    profile["exclude_suggestions"] = []
    profile["leakage_columns"] = []
    columns = {}
    
    # To add per-column:
    # 	(numeric) min, max, mean, std, more?
    # 	(categorical) top, freq	Top category, more?
    # 	(datetime) min, max

    for column in df.columns:
        columns[column] = _analyse_column(df[column])
        if columns[column]["is_unique"]:
            profile["id_candidates"].append(column)
        if columns[column]["is_empty"] or columns[column]["is_constant"] or columns[column]["exclude_for_analysis"]:
            profile["drop_suggestions"].append(column)
        
    profile["columns"] = columns
    return profile

if __name__ == "__main__":
    df = get_dataframe("./test_dataset.csv")
    profile = suggest_profile(pd.DataFrame(df))
    print(df["gender"])
    # print(profile)
    
    