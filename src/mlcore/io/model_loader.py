from joblib import load
from pathlib import Path
from src.db.db import get_ml_problem, get_model

def load_model(
    model_uri: str | None = None,
    problem_id: str | None = None,
    model_id: str | None = "production",
    base_dir: str = "./testdata/models",
):
    """
    Load a trained model either from a given URI or based on
    problem and model identifiers.
    """
    if not model_uri and not problem_id:
        raise ValueError("Not specified which model to load. Provide a problem_id or a model_uri.")
    
    try:
        if model_uri:
            model_path = Path(model_uri)
        else:
            if model_id == "production":
                problem = get_ml_problem(problem_id)
                model_id = problem.get("current_model_id", False)
                model = get_model(model_id)
                model_path = model.get("uri", False)
            else:
                model_path = Path(base_dir) / problem_id / model_id / "model.joblib"
        model = load(model_path)
        return model
    except Exception as e:
        print(f"Failed to load model: {e}")
        raise