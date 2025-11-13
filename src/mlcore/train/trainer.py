from src.mlcore.io.synthetic_generators import gen_classification
from src.mlcore.io.preset_loader import loader
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from typing import Literal

def train(
    task: str,
    X: list,
    y: list,
    semantic_types: dict,
    algorithm: str = "auto",
    train_mode: Literal["fast", "balanced", "accurate"] = "balanced",
    random_seed: int = 42,    
)-> str:
    
    categorical = semantic_types["categorical"]
    numeric = semantic_types["numeric"]
    boolean = semantic_types["boolean"]
    
    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, stratify=y, random_state= random_seed
        )
    
    build_model = loader(task, algorithm)
    
    # Missing metadata handling - filling
    model, metadata = build_model(categorical, numeric, boolean, train_mode)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return classification_report(y_test, y_pred)






