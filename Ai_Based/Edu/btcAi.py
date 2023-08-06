# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 20:06:37 2023

@author: furka
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.model_selection import train_test_split


df = pd.read_csv("BTCUSDT_Data.csv")

x = df[[ "Price_Direction", "O", "h",
        "l", "v", "qav", "num_trades", "taker_base_vol", "taker_quote_vol"]]
y = df['C']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.01,
                                                    random_state=3)

regr = linear_model.LinearRegression()
regr.fit(x, y)

prediction = regr.predict(x_test)




y_test = y_test.reset_index()
y_test.drop('index', inplace=True, axis=1)




plt.scatter([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], prediction, color= "green")
plt.scatter([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], y_test, color= "red")
plt.show()

import statsmodels.api as sm 

X_train_opt = np.append(arr = np.ones((1990,1)).astype(int), values = df,
                        axis = 1) 

x_l = df.iloc[:,[1, 2, 3, 4, 5, 6, 7, 8, 9]].values

regressor_OLS = sm.OLS(y, x_l).fit()

print(regressor_OLS.summary())


