
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
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix

def ridge(X, y):
    print("Calling ridge model.....\n\n")
    X_polynomial = PolynomialFeatures(1).fit_transform(X)
    X_polynomial = np.array(X)
    kf = KFold(n_splits=5)
    error = []
    ridge_error_c = []
    for C in C_range:
        #print("C = " + str(C))
        for train, test in kf.split(X_polynomial):
            model = linear_model.Ridge(alpha=(1/(2*C)))
            model.fit(X_polynomial[train], y[train])
            preds = model.predict(X_polynomial[test])
            error.append(metrics.mean_squared_error(y[test], preds))
            #print("Intercept = " + str(model.intercept_) + "\nCo-efficients = "
            #      + str(model.coef_) + "\nSquare Error = " + str(mean_squared_error(y[test], preds)))
        ridge_error_c.append(np.mean(error))
    #print("Final Ridge\n")
    model = linear_model.Ridge(alpha=(1/(2*0.5))).fit(X_polynomial, y)
    preds = model.predict(X_polynomial)
    #print("Intercept = " + str(model.intercept_) + "\nCo-efficients = "
    #      + str(model.coef_) + "\nSquare Error = " + str(mean_squared_error(y, preds)))
    return ridge_error_c