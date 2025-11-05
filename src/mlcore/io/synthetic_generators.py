from sklearn.datasets import make_classification, make_regression

def gen_classification(n_samples, n_classes, n_informative, random_state):
    X, y = make_classification(n_samples= n_samples, n_classes= n_classes, n_informative= n_informative, random_state= random_state)
    return X, y

def gen_regression(n_samples, n_classes, random_state):
    X, y = make_regression(n_samples= n_samples, n_classes= n_classes, random_state= random_state)
    return X, y