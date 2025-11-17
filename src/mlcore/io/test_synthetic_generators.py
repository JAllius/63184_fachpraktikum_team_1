from .synthetic_generators import gen_classification
from numpy import ndarray


def test_gen_classification():
    X, y = gen_classification(5000, 3, 3, 42)
    assert isinstance(X, ndarray)
    assert isinstance(y, ndarray)
