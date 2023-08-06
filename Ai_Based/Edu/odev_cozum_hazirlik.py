
#1. kutuphaneler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.model_selection import train_test_split

df = pd.read_csv("odev_tenis.csv")

outlook = df[["outlook"]]
windy = df[["windy"]]
play = df[["play"]]

ohe = OneHotEncoder()
  
outlook = ohe.fit_transform(df[['outlook']]).toarray()

outlook = pd.DataFrame(pd.DataFrame(outlook, columns=['overcast', 'rainy',
                                                      "sunny"]))
df = pd.concat([outlook, df], axis=1)
df.drop('outlook', inplace=True, axis=1)

le = preprocessing.LabelEncoder()
windy = le.fit_transform(df['windy'])
windy =  pd.DataFrame(pd.DataFrame(windy, columns=['windy']))
df.drop('windy', inplace=True, axis=1)
df = pd.concat([windy, df], axis=1)

play = le.fit_transform(df['play'])
play =  pd.DataFrame(pd.DataFrame(play, columns=['play']))
df.drop('play', inplace=True, axis=1)
df = pd.concat([play, df], axis=1)


x = df[["windy",  "overcast",  "rainy",  "sunny",  "temperature"]]
y = df['play']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20,
                                                    random_state=3)

regr = linear_model.LinearRegression()
regr.fit(x, y)

prediction = regr.predict(x_test)

import statsmodels.api as sm 

X_train_opt = np.append(arr = np.ones((14,1)).astype(int), values = df,
                        axis = 1) 

x_l = df.iloc[:,[1,2,3,4,5]].values

regressor_OLS = sm.OLS(y, x_l).fit()

print(regressor_OLS.summary())

