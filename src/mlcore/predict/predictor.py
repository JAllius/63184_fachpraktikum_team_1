import pandas as pd
from pathlib import Path
from src.mlcore.io.data_reader import get_dataframe_from_csv
from src.mlcore.io.model_loader import load_model
from src.mlcore.io.metadata_loader import load_metadata

def predict(
    input: pd.DataFrame | None = None,
    input_uri: str| None = None,
    problem_id: str | None = None,
    model_id: str | None = "production",
    model_uri: str | None = None,   
)-> str:
    
    if not input and not input_uri:
        raise ValueError("No input dataframe was specified. Provide an input or an input_uri.")
    
    if not model_uri and not problem_id:
        raise ValueError("Not specified which model to load. Provide a problem_id or a model_uri.")
    
    if input_uri:
        X = get_dataframe_from_csv(input_uri)
    else:
        X = input    

    if model_uri:
        model = load_model(model_uri= model_uri)
        model_path = Path(model_uri)
        metadata_path = model_path.with_name("metadata.json")
        metadata = load_metadata(metadata_path)
        target = metadata.get("target")
    else:
        if model_id == "production":
            
            # READ DB (PROBLEM_ID) -> PRODUCTION: URI & TARGET (COLUMN)
            replace_this_line = 1
            
            model_path = replace_this_line
            model = load_model(model_uri= model_path)
            metadata_path = model_path.with_name("metadata.json")
            metadata = load_metadata(metadata_path)
            target = metadata.get("target")
        else:
            model = load_model(problem_id= problem_id, model_id= model_id)
            metadata = load_metadata(problem_id= problem_id, model_id= model_id)
            target = metadata.get("target")
            
    if target in X.columns:
        X.drop(columns= target)
    
    ### MISSING ###
    # Check schema snapshot and compare with X
    ### END MISSING ###
    
    y_pred = model.predict(X)
    
    prediction_summary = {
        "X": X,
        "y_pred": y_pred,
        "model_metadata": metadata,        
    }           

    return X, y_pred, prediction_summary

