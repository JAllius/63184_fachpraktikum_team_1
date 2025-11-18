import numpy as np
import shap

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
    n_ref = max(1, int(len(X_train) * pct_ref))
    # Equivalent to .sample method of pandas
    idx_ref = rng.choice(len(X_train), size=n_ref, replace=False)
    X_ref = X_train[idx_ref]
    

    # Explanation sample percentage (5–20%)
    pct_explain = rng.integers(5, 21) / 100.0
    n_explain = max(1, int(len(X_test) * pct_explain))
    # Equivalent to .sample method of pandas
    idx_explain = rng.choice(len(X_train), size=n_ref, replace=False)
    X_explain = X_train[idx_explain]
    
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

