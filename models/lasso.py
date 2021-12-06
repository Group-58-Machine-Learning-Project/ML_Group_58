import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import KFold
from scraping.formatting import csv_for_models

def normalize(arr):
    min = np.min(arr)
    max = np.max(arr)
    arr = arr - min
    arr = arr / (max - min)
    arr = (arr * 2.0) - 1.0
    return arr

def lasso():
    print("\nCalling lasso model")
    ber, price, bedrooms, bathrooms, distance = csv_for_models()

    X = np.column_stack((bedrooms, bathrooms, distance, ber))
    y = price

    polynomial = PolynomialFeatures(5)
    X = polynomial.fit_transform(X)

    mean = []
    std = []
    cValues = [0.01, 1, 10, 30, 50, 100, 150, 200, 300, 500, 1000, 2000, 2500]
    kf = KFold(n_splits=5)

    for C in cValues:

        model = Lasso(alpha=(1/(2*C)))
        temp = []

        for train, test in kf.split(X):

            model.fit(X[train], y[train])
            ypred = model.predict(X[test])
            error = mean_squared_error(y[test], ypred)
            temp.append(error)

        mean.append(np.array(temp).mean())
        std.append(np.array(temp).std())

    plt.errorbar(cValues, mean, yerr=std, label="LASSO MSE Error")
    plt.xlabel("C")
    plt.ylabel("Mean Square Error")
    plt.title("MSE of LASSO Model with Various C's")
    plt.legend()
    plt.show()

    # Best C = 100
    print("LASSO Best MSE Among C Values = " + str(np.min(mean)))

    # Final Model
    model = Lasso(alpha=(1/(2*100)))
    model.fit(X, y)
    ypred = model.predict(X)
    print("Square Error = " + str(mean_squared_error(y, ypred)))

    return mean, std

