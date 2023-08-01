# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 20:06:37 2023

@author: furka
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


df = pd.read_csv("Rendered_Data_4h.csv")
df.set_index("Index", inplace=True)

examine_df = pd.DataFrame(columns=["Now", "Future","Percentage", "Prediction", "Succes"])

date_line = 11800
# budget = 100
# btc_count = 0
# first_order = True

train_df = df.iloc[:date_line]

x = train_df[[ "now", "h", "l", "v", "qav","num_trades","taker_base_vol",
              "taker_quote_vol"]]
y = train_df["Percentage"]

from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(x, y)

backtest_df = df.loc[date_line:]

predict_df = backtest_df.copy()

del predict_df["Future"]
del predict_df["Percentage"]
del predict_df["Open_Time"]
del predict_df["Close_Time"]

# last_order = None
# sell_y = []

# future_y = []
# predict_y = []

# sold_y = []
# sold_x = []
# bought_y = []
# bought_x = []

for i in range(len(backtest_df)):
    
    now = backtest_df.iloc[i].now
    future = backtest_df.iloc[i].Future
    prediction =  regr.predict(predict_df.iloc[[i]])[0]+0.009
    percentage = future*100/now - 100
    
    # future_y.append(percentage)
    # predict_y.append(prediction)
    
    if percentage > 0 and prediction > 0:
        succes = 1
    elif percentage < 0 and prediction < 0:
        succes = 1
    else:
        succes = 0
    
    # examine_df.loc[i] = [now, future, prediction, succes ] 
    examine_df.loc[i] = [now, future, percentage, prediction, succes] 
    
    # if budget == 0:
    #     sell_y.append(btc_count * now)
    # else:
    #     sell_y.append(budget)

    
    # if now > prediction:
    #     if last_order != "buy" :
    #         print("buy")
    #         btc_count = budget/now
    #         budget = 0
    #         print(btc_count)
    #         last_order = "buy"
    #         first_order = False
            
    #         bought_x.append(backtest_df.iloc[i].Close_Time)
    #         bought_y.append(now)   
            
    # else:
    #     if last_order != "sell" and first_order != True:
    #         print("sell")
    #         budget = btc_count * now
    #         btc_count = 0
    #         print(budget)
    #         last_order = "sell"
            
    #         sold_x.append(backtest_df.iloc[i].Close_Time)
    #         sold_y.append(now)
        
zero_count = (examine_df['Succes'] == 0).sum()
one_count = (examine_df['Succes'] == 1).sum()
print("Succes Rate: "+str(100*one_count/(zero_count+one_count))+"%")

# x = []
# y = []

# for i in backtest_df.iterrows():
#     x.append(i[1]["Close_Time"])
#     y.append(i[1]["now"])
# plt.plot(x, y, color="green")

# plt.plot(x, sell_y, color = "red")

# plt.plot(x, future_y, color = "red")
# plt.plot(x, predict_y, color = "blue")

# plt.scatter(sold_x, sold_y, color = "red")
# plt.scatter(bought_x, bought_y, color = "green")

# examine_df.to_csv("examine_df.csv")






