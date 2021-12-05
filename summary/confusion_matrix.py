# Might change the name of this file later as there isnt much point
# in splitting everything up so much.
# Will probability put confusion martix, standard error and ROC all in here

import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import mean_squared_error

def dummy_baseline(X, y):
    X_polynomial = np.array(X)
    print("Dummy - Most Frequent")
    dummy = DummyClassifier(strategy="uniform").fit(X_polynomial, y)
    preds = dummy.predict(X_polynomial)
    return mean_squared_error(y, preds)