import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import KFold

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

df = pd.read_csv("scraping/houses.csv")

ber = np.array(df.iloc[:,6])
price = np.array(df.iloc[:,1])
bedrooms = np.array(df.iloc[:,2])
bathrooms = np.array(df.iloc[:,3])
distance = np.array(df.iloc[:,5])

minPrice = np.min(price)
maxPrice = np.max(price)
price = normalize(price)
bedrooms = normalize(bedrooms)
bathrooms = normalize(bathrooms)
distance = normalize(distance)
ber = normalize(ber)

X = np.column_stack((bedrooms, bathrooms, distance, ber))
y = price
weightFunctions = ['uniform', gaussianKernel10, gaussianKernel100, gaussianKernel500]

for wf in weightFunctions:

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

    print(np.min(mean))

    plt.errorbar(kValues, mean, yerr=std)
    plt.xlabel("K")
    plt.ylabel("Mean Square Error")
    plt.show()
