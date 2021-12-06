import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from scraping.formatting import csv_for_models

def ridge():
    print("\nCalling ridge model")
    ber, price, bedrooms, bathrooms, distance = csv_for_models()

    X = np.column_stack((bedrooms, bathrooms, distance, ber))
    y = price

    polynomial = PolynomialFeatures(5)
    X = polynomial.fit_transform(X)

    mean = []
    std = []
    # Best C = 0.01
    cValues = [0.01, 1, 10, 30, 50, 100, 150, 200]
    kf = KFold(n_splits=5)

    for C in cValues:

        model = linear_model.Ridge(alpha=(1 / (2 * C)))
        temp = []

        for train, test in kf.split(X):
            model.fit(X[train], y[train])
            ypred = model.predict(X[test])
            error = mean_squared_error(y[test], ypred)
            temp.append(error)

        mean.append(np.array(temp).mean())
        std.append(np.array(temp).std())

    plt.errorbar(cValues, mean, yerr=std, label="Ridge MSE Error")
    plt.xlabel("C")
    plt.ylabel("Mean Square Error")
    plt.title("MSE of Ridge Model with Various C's")
    plt.legend()
    plt.show()

    print("Ridge Best MSE Among C Values = " + str(np.min(mean)))

    # Final Model
    model = linear_model.Ridge(alpha=(1 / (2 * 0.01)))
    model.fit(X, y)
    ypred = model.predict(X)
    print("Square Error = " + str(mean_squared_error(y, ypred)))

    return mean, std


