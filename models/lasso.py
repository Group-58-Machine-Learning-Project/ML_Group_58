import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

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

plt.errorbar(cValues, mean, yerr=std)
plt.xlabel("C")
plt.ylabel("Mean Square Error")
plt.show()

print(np.min(mean))

model = Lasso(alpha=(1/(2*1000)))
model.fit(X, y)
