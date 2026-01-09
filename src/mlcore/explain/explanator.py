import numpy as np
import shap
from scipy.sparse import issparse

def _force_2D(X):
    # Force 2D to avoid errors due to dimension mismatch
    if issparse(X):
        # Transform to CSR and to array to make it dense
        X = X.tocsr().toarray()
    else:
        # Transform to np array to use .ndim and .reshape()
        X = np.asarray(X)
    if X.ndim == 1:
        X = X.reshape(1, -1)
    return X

def explain_model(
    task: str,
    model,
    X_train: np.ndarray,
    X_test: np.ndarray,
    random_seed: int = 42,    
    )-> dict:
    explanation_summary = {}
    rng = np.random.default_rng(random_seed)
    
    # Reducing samples by a random percentage to reduce running time of Explain
    # Background sample percentage (1–10%)
    pct_ref = rng.integers(1, 11) / 100.0
    n_rows = X_train.shape[0]
    n_ref = max(1, int(n_rows * pct_ref))
    # Equivalent to .sample method of pandas
    idx_ref = rng.choice(n_rows, size=n_ref, replace=False)
    X_ref = X_train[idx_ref]
    
    # Explanation sample percentage (5–20%)
    pct_explain = rng.integers(5, 21) / 100.0
    n_rows_explain = X_test.shape[0]
    n_explain = max(1, int(n_rows_explain * pct_explain))
    # Equivalent to .sample method of pandas
    idx_explain = rng.choice(n_rows_explain, size=n_explain, replace=False)
    X_explain = X_test[idx_explain]
    
    # Force 2D due to error with sparce data and dimension mismatch after OHE
    X_ref = _force_2D(X_ref)
    X_explain = _force_2D(X_explain)   

    if task == "classification":
        explanation_summary = classification_explanation(model, X_ref, X_explain)
    elif task == "regression":
        explanation_summary = regression_explanation(model, X_ref, X_explain)
    else:
        raise ValueError(f"Invalid task: '{task}'. Expected 'classification' or 'regression'.")
    
    return explanation_summary

def classification_explanation(
    model,
    X_ref: np.ndarray,
    X_explain: np.ndarray,
    ):
    explainer = shap.Explainer(model.predict_proba, X_ref)
    shap_values = explainer(X_explain)
    return shap_values

def regression_explanation(
    model, X_ref: np.ndarray,
    X_explain: np.ndarray,
    ):
    explainer = shap.Explainer(model.predict, X_ref)
    shap_values = explainer(X_explain)
    return shap_values

