import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import KFold
from scraping.formatting import csv_for_models

def gaussianKernel10(distances):
    weights = np.exp(-10*(distances**2))
    return weights/np.sum(weights)

def gaussianKernel100(distances):
    weights = np.exp(-100*(distances**2))
    return weights/np.sum(weights)

def gaussianKernel500(distances):
    weights = np.exp(-500*(distances**2))
    return weights/np.sum(weights)

def normalize(arr):
    min = np.min(arr)
    max = np.max(arr)
    arr = arr - min
    arr = arr / (max - min)
    arr = (arr * 2.0) - 1.0
    return arr

def kNN():
    print("\nCalling kNN model")
    ber, price, bedrooms, bathrooms, distance = csv_for_models()

    X = np.column_stack((bedrooms, bathrooms, distance, ber))
    y = price
    weightFunctions = ['uniform', gaussianKernel10, gaussianKernel100, gaussianKernel500]
    weightFNames = ['uniform', 'Sigma = 10', 'Sigma = 100', 'Sigma = 500']

    k_errors = []
    for wf, name in zip(weightFunctions, weightFNames):

        mean = []
        std = []
        kValues = range(1,15)
        kf = KFold(n_splits=5)

        for k in kValues:

            model = KNeighborsRegressor(n_neighbors=k, weights=wf)
            temp = []

            for train, test in kf.split(X):

                model.fit(X[train], y[train])
                ypred = model.predict(X[test])
                error = mean_squared_error(y[test], ypred)
                temp.append(error)

            mean.append(np.array(temp).mean())
            std.append(np.array(temp).std())

        #print(np.min(mean))
        plt.errorbar(kValues, mean, yerr=std, label=f"kNN MSE ({name})")
        plt.title("MSE of kNN")
        plt.xlabel("K")
        plt.ylabel("Mean Square Error")
        plt.legend()
        plt.show()

    # Best of these is k = 6, with weight of 'uniform'
    for k in kValues:
        model = KNeighborsRegressor(n_neighbors=k, weights='uniform')
        temp = []
        for train, test in kf.split(X):
            model.fit(X[train], y[train])
            ypred = model.predict(X[test])
            error = mean_squared_error(y[test], ypred)
            temp.append(error)

        mean.append(np.array(temp).mean())
        std.append(np.array(temp).std())

    return mean, std
