# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 20:06:37 2023

@author: furka
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


df = pd.read_csv("Price_Data_Daily/Rendered_Data.csv")
# df = pd.read_csv("Price_Data_2/BTCUSDT_Data.csv")

df.set_index("Index", inplace=True)

x = df[[ "now", "l", "h","v","qav","num_trades","taker_base_vol",
        "taker_quote_vol"]]

y = df["Future"]



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.01,
                                                    random_state=43)


from sklearn import linear_model

regr = linear_model.LinearRegression()
regr.fit(x, y)


x_test = x_test.sort_index()
y_test = y_test.sort_index()
x_test = x_test.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)


prediction = regr.predict(x_test)

import statsmodels.api as sm 

X_train_opt = np.append(arr = np.ones((2004,1)).astype(int), values = df,
                        axis = 1) 

x_l = df.iloc[:,[0,1,2,4,5,7,8,9,10]]

regressor_OLS = sm.OLS(y, x_l).fit()
# print(regressor_OLS.summary())

sapma = []

for i in range(12):
    
    test = y_test[i]
    predict = prediction[i]
    
    percentage = predict * 100 / test
    
    if predict > test:
        sapma.append(percentage - 100)
    else:
        sapma.append(100 - percentage)
    
def Average(lst):
    return sum(lst) / len(lst)
    
print("Sapma: "+str(Average(sapma)))



plt.plot(range(len(y_test)), y_test, color="blue")
plt.plot(range(len(y_test)), prediction, color="red")


