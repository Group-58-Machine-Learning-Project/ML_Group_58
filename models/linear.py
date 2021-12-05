
C_range = [0.001, 0.01, 0.1, 1, 10, 50, 100, 1000, 10000]
import numpy as np
from sklearn.linear_model import *
from sklearn import metrics
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import pandas as pd
# currentAlpha = 1 / (2 * c)  # alpha value for current model using current c value
# la_model = Lasso(alpha=currentAlpha)



def linear(X, y):
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import confusion_matrix
    print("Calling linear model")
    X_polynomial = PolynomialFeatures(1).fit_transform(X)
    X_polynomial = np.array(X)
    kf = KFold(n_splits=5)
    error = []
    for train, test in kf.split(X_polynomial):
        model = LinearRegression()
        model.fit(X_polynomial[train], y[train])
        preds = model.predict(X_polynomial[test])
        error.append(metrics.mean_squared_error(y[test], preds))
    linear_error = np.mean(error)
    model = LinearRegression().fit(X_polynomial, y)
    preds = model.predict(X_polynomial)
    #print("Intercept = " + str(model.intercept_) + "\nCo-efficients = "
    #      + str(model.coef_) + "\nSquare Error = " + str(mean_squared_error(y, preds)))
    return linear_error


def format_accommodation(accommodation):
    prices, bedrooms, bathrooms, distance, BER = [], [], [], [], []
    for index in accommodation:
        if(index['BER'] != "NA"):
            prices.append(index['price'])
            bedrooms.append(index['bedrooms'])
            bathrooms.append(index['bathrooms'])
            distance.append(index['distance'])
            BER.append(index['BER'])
        else:
            print("BER of NA avoided.")
    return [prices, bedrooms, bathrooms, distance, BER]