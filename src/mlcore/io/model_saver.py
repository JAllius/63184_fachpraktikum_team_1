from joblib import dump
from pathlib import Path
import json
import os

def save_model(
    model,
    metadata: dict,
    problem_id: str,
    model_id: str,
    base_dir: str = "./testdata/models",
)-> str:
    base_path = Path(base_dir)
    model_dir = base_path / problem_id / model_id
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / "model.joblib"
    metadata_path = model_dir / "metadata.json"
    
    # Store POSIX-style path in metadata for portability (works in Linux and Windows)
    metadata["model_uri"] = model_path.as_posix()
    
    try:
        dump(model, model_path, compress=3)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
        # print("Model saved successfully.")
        return model_path
    except Exception as e:
        print(f"Failed to save model: {e}")
        raise

    

    
