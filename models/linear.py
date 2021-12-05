
C_range = [0.01, 0.1, 1, 10, 50, 100, 1000, 10000]
import numpy as np
from sklearn.linear_model import *
from sklearn import metrics
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# currentAlpha = 1 / (2 * c)  # alpha value for current model using current c value
# la_model = Lasso(alpha=currentAlpha)

def linear(accommodation):
    data = format_accommodation(accommodation)
    y = np.arange(data[0]).reshape(-1, 1)
    x = np.arange(data[1], data[2], data[3], data[4]).reshape(-1, 1)
    print("Calling linear model")
    kf = KFold(n_splits=5)
    model = LinearRegression()
    x_poly = PolynomialFeatures(1).fit_transform(x)
    model.fit(x_poly, np.array(data[3]))
    #predications = model.predict(np.array([data[3]]))
    # for train, test in kf.split(data[3]):
    #     model = LinearRegression()
    #     model.fit(np.array([data[3]]), np.array([data[0]]))
    #     model.fit(np.array(data[3])[train], np.array([data[0]])[train])
    #     predications = model.predict(np.array([data[3]][train]))

    # plt.scatter(data[0], data[3], c='r', label="Prices VS Distance")
    # plt.scatter(predications, data[3], c='g', marker='+', label="Predictions VS Distance")
    # plt.title("Prices VS Distance")
    # plt.xlabel("Price")
    # plt.ylabel("Distance")
    # plt.show()
    # print("Yeah")
    # print("Yeah 2")

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