

import pandas as pd

budget = 1000
date_line = 1500


df = pd.read_csv("Rendered_Data_Daily.csv")

df = df[date_line:]

for i in df["Percentage"]:
    if i > 0:
        budget = budget + budget * i / 100
        
print(budget)
