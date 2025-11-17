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
    path = os.path.join(base_dir, problem_id, model_id)
    os.makedirs(path, exist_ok=True)

    model_path = os.path.join(path, "model.joblib")
    metadata_path = os.path.join(path, "metadata.json")
    
    try:
        from joblib import dump
        dump(model, model_path, compress=3)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
        # print("Model saved successfully.")
        return model_path
    except Exception as e:
        print(f"Failed to save model: {e}")
        raise

    

    
