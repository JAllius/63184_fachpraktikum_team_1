from joblib import dump
from pathlib import Path

def save_model(
    model,
    uri: str,
)-> str:
    base_path = Path(uri)
    base_path.mkdir(parents=True, exist_ok=True)

    model_path = base_path / "model.joblib"

    try:
        dump(model, model_path, compress=3)
        return "Success"
    except Exception as e:
        print(f"Failed to save model: {e}")
        raise

    

    
