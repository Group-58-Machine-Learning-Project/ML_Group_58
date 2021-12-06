import numpy as np
from sklearn.linear_model import *
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from scraping.formatting import csv_for_models

def linear():
    print("Calling linear model")
    ber, price, bedrooms, bathrooms, distance = csv_for_models()

    X = np.column_stack((bedrooms, bathrooms, distance, ber))
    y = price

    polynomial = PolynomialFeatures(5)
    X = polynomial.fit_transform(X)

    mean = []
    std = []
    kf = KFold(n_splits=5)

    temp = []
    for train, test in kf.split(X):
        model = LinearRegression()
        model.fit(X[train], y[train])
        ypred = model.predict(X[test])
        error = mean_squared_error(y[test], ypred)
        temp.append(error)

    print("Linear:")
    print("Linear Min MSE Among Training:" + str(np.min(np.array(temp))))

    # Final Model
    model = LinearRegression()
    model.fit(X, y)
    ypred = model.predict(X)
    print("Intercept = " + str(model.intercept_) +
          #"\nCo-efficients = " + str(model.coef_) +
          "\nSquare Error = " + str(mean_squared_error(y, ypred)))

    return mean_squared_error(y, ypred)

