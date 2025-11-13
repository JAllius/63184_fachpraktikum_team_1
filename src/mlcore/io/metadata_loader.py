import json
from pathlib import Path

def load_metadata(
    metadata_uri: str,
    problem_id: str | None = None,
    model_id: str | None = "production",
    base_dir: str = "./testdata/models",
)-> dict:
    """
    Load the metadata of a model either from a given URI or based on
    problem and model identifiers.
    """
    if not metadata_uri:
        raise ValueError("No metadata_uri was provided. Provide a metadata_uri.")
    
    try:
        if metadata_uri:
            with open(metadata_uri, "r") as f:
                metadata = json.load(f)
        else:
            if model_id == "production":
                
                # READ DB (PROBLEM_ID) -> PRODUCTION: URI
                replace_this_line = 1
                
                model_path = Path(replace_this_line)
                metadata_path = model_path.with_name("metadata.json")
            else:
                metadata_path = Path(base_dir) / problem_id / model_id / "metadata.json"
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
        return metadata
    except Exception as e:
        print(f"Failed to load metadata: {e}")
        raise