C_range = [0.01, 0.1, 1, 10, 50, 100, 1000, 10000]
import numpy as np
from sklearn.linear_model import *
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# currentAlpha = 1 / (2 * c)  # alpha value for current model using current c value
# la_model = Lasso(alpha=currentAlpha)

def linear(accommodation):
    data = format_accommodation(accommodation)
    print("Calling linear model")
    model = LinearRegression()
    model.fit(np.array([data[3]]), np.array([data[0]]))
    predications = model.predict(np.array([data[3]]))

    plt.scatter(data[0], data[3], c='r', label="Prices VS Distance")
    plt.scatter(predications, data[3], c='g', marker='+', label="Predictions VS Distance")
    plt.title("Prices VS Distance")
    plt.xlabel("Price")
    plt.ylabel("Distance")
    plt.show()
    print("Yeah")
    print("Yeah 2")

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