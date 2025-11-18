from .trainer import train
from pathlib import Path

def test_trainer():
    problem_id = "7f3c6b2a-4c1e-4f7b-bb59-3c9e5c1f0e8d"
    model_uri = train(problem_id, "random_forest")
    assert isinstance(model_uri, Path)

if __name__ == "__main__":
    test_trainer()
