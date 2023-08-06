from matplotlib import pyplot as plt
import pandas as pd

x = []
y = []

data = pd.read_csv("BTC Tools/Ar-Ge/Seasons/BearSeason---59.csv")
for i in data.iterrows():
    x.append(i[1]["Open_Time"])
    y.append(i[1]["O"])
plt.plot(x, y, color = "green")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()