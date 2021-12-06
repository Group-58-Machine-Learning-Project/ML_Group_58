import numpy as np
from sklearn.linear_model import *
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from scraping.formatting import csv_for_models
from matplotlib import pyplot as plt

def linear():
    print("Calling linear model")
    ber, price, bedrooms, bathrooms, distance = csv_for_models()

    X = np.column_stack((bedrooms, bathrooms, distance, ber))
    y = price

    mean = []
    std = []
    polyDegrees = range(1, 5)

    for degree in polyDegrees:
        polynomial = PolynomialFeatures(degree)
        X1 = polynomial.fit_transform(X)

        kf = KFold(n_splits=5)

        temp = []
        for train, test in kf.split(X1):
            model = LinearRegression()
            model.fit(X1[train], y[train])
            ypred = model.predict(X1[test])
            error = mean_squared_error(y[test], ypred)
            temp.append(error)

        mean.append(np.array(temp).mean())
        std.append(np.array(temp).std())

    plt.errorbar(polyDegrees, mean, yerr=std, label="Linear MSE")
    plt.xlabel("Polyonmial Degree")
    plt.ylabel("Mean Square Error")
    plt.title("MSE of Linear Model")
    plt.legend()
    plt.show()

    print("Linear:")
    print("Linear Min MSE Among Training: " + str(np.min(np.array(mean))))

    # Final Model
    model = LinearRegression()
    model.fit(X, y)
    ypred = model.predict(X)
    print("Intercept = " + str(model.intercept_) +
          "\nCo-efficients = " + str(model.coef_) +
          "\nSquare Error = " + str(mean_squared_error(y, ypred)))

    return mean, std

