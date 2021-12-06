import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import mean_squared_error
from scraping.formatting import csv_for_models
from sklearn.preprocessing import PolynomialFeatures

def dummy_():
    print("Dummy - Most Frequent")
    ber, price, bedrooms, bathrooms, distance = csv_for_models()

    X = np.column_stack((bedrooms, bathrooms, distance, ber))
    y = price

    polynomial = PolynomialFeatures(5)
    X = polynomial.fit_transform(X)

    model = DummyClassifier(strategy="uniform").fit(X, y)
    ypred = model.predict(X)
    error = mean_squared_error(y, ypred)

    print("Dummy:")
    print("Dummy MSE:" + str(error))

    return error