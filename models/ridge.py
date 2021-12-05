
C_range = [0.01, 0.1, 1, 10, 50, 100, 1000, 10000]
import numpy as np
from sklearn.linear_model import *
from sklearn import metrics
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
# currentAlpha = 1 / (2 * c)  # alpha value for current model using current c value
# la_model = Lasso(alpha=currentAlpha)

def ridge(X, y):
    print("Calling linear model")
    X_polynomial = PolynomialFeatures(1).fit_transform(X)
    kf = KFold(n_splits=5)
    error = []
    ridge_error = []
    for C in C_range:
        for train, test in kf.split(X_polynomial):
            model = linear_model.Ridge(alpha=(1/(2*C)))
            model.fit(X_polynomial[train], y[train])
            preds = model.predict(X_polynomial[test])
            error.append(metrics.mean_squared_error(y[test], preds))
        ridge_error.append(np.mean(error))
    return ridge_error