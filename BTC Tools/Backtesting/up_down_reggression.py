#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 16:56:01 2023

@author: furkan
"""

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("Rendered_Data_4h.csv")
df.set_index("Index", inplace=True)

direction = lambda x : +1 if(x > 0) else -1

df.insert(5,"Direction",[ direction( x[1].Future*100/x[1].now - 100 ) 
                          for x in df.iterrows() ] ,True )

examine_df = pd.DataFrame(columns=["Now", "Future","Percentage", "Prediction", "Succes"])

date_line = 11000

train_df = df.iloc[:date_line]

x = train_df[["Open_Time", "Close_Time", "now", "h", "l", "v", "qav","num_trades","taker_base_vol",
              "taker_quote_vol"]]
y = train_df["Direction"]

from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(x, y)

backtest_df = df.loc[date_line:]

predict_df = backtest_df.copy()

del predict_df["Future"]
del predict_df["Percentage"]
del predict_df["Direction"]

future_y = []
predict_y = []

for i in range(len(backtest_df)):
    
    now = backtest_df.iloc[i].now
    future = backtest_df.iloc[i].Future
    direction = backtest_df.iloc[i].Direction
    prediction =  regr.predict(predict_df.iloc[[i]])[0]
    percentage = future*100/now - 100
    
    future_y.append(direction)
    predict_y.append(prediction)
    
    
    if direction > 0 and prediction > 0:
        succes = 1
    elif direction < 0 and prediction < 0:
        succes = 1
    else:
        succes = 0
    
    examine_df.loc[i] = [now, future, percentage, prediction, succes] 
    
        
zero_count = (examine_df['Succes'] == 0).sum()
one_count = (examine_df['Succes'] == 1).sum()
print("Succes Rate: "+str(100*one_count/(zero_count+one_count))+"%")

x = []
y = []

for i in backtest_df.iterrows():
    x.append(i[1]["Close_Time"])
    y.append(i[1]["now"])
    
plt.plot(x, future_y, color = "red")
plt.plot(x, predict_y, color = "blue")
