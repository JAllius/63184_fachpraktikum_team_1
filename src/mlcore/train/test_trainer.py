from .trainer import gen_classification, classification
from numpy import ndarray

def test_gen_classification():
    x, y = gen_classification(5000, 3, 3, 42)
    assert isinstance(x, ndarray)
    assert isinstance(y, ndarray) 
    print(classification(x, y, 42))

def test_classification():
    x, y = gen_classification(5000, 3, 3, 42)
    out = classification(x, y, 42)
    assert isinstance(out, str)