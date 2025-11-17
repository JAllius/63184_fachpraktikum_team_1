from .trainer import train
from ..io.synthetic_generators import gen_classification
from numpy import ndarray
import pytest


# TODO: update testcase
@pytest.mark.skip("Test deprecated after changes to parameters for train()")
def test_gen_classification():
    X, y = gen_classification(5000, 3, 3, 42)
    assert isinstance(X, ndarray)
    assert isinstance(y, ndarray)
    print(train(X, y, 42))


# TODO: update testcase
@pytest.mark.skip("Test deprecated after changes to parameters for train()")
def test_classification():
    X, y = gen_classification(5000, 3, 3, 42)
    out = train(X, y, 42)
    assert isinstance(out, str)


def test_trainer():
    problem_id = "7f3c6b2a-4c1e-4f7b-bb59-3c9e5c1f0e8d"
    model_uri = train(problem_id, "random_forest")
    assert isinstance(model_uri, str)


if __name__ == "__main__":
    test_trainer()
