from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, mean_absolute_percentage_error, r2_score
import pandas as pd

def calculate_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
    task: str,
)-> dict:
    
    if task == "classification":
        metrics = classification_metrics(y_true, y_pred)
    elif task == "regression":
        metrics = regression_metrics(y_true, y_pred)
    else:
        raise ValueError(f"Invalid task: '{task}'. Expected 'classification' or 'regression'.")
            

def classification_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
)-> dict:
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
    }
    return metrics

def regression_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
)-> dict:
    metrics = {
        "mae": mean_absolute_error(y_true, y_pred),
        "mse": mean_squared_error(y_true, y_pred),
        "rmse": root_mean_squared_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
        "mape": mean_absolute_percentage_error(y_true, y_pred),
    }
    return metrics