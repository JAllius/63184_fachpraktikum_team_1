from joblib import load
from pathlib import Path

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
            model = load(model_uri)
            return model
        else:
            if model_id == "production":
                
                # READ DB (PROBLEM_ID) -> PRODUCTION: URI
                replace_this_line = 1
                
                model_path = replace_this_line
                model = load(model_path)
                return model
            else:
                path = Path(base_dir) / problem_id / model_id / "model.joblib"
                model = load(path)
                return model
    except Exception as e:
        print(f"Failed to load model: {e}")
        raise