from joblib import dump
from pathlib import Path
import json

def save_model(
    model,
    metadata: dict,
    base_dir: str = "./testdata/models/problem_id/model_id",
)-> str:
    model_path = Path(base_dir) / "model.joblib"
    metadata_path = Path(base_dir) / "metadata.json"
    
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

    

    
