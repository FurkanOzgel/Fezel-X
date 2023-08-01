import pandas as pd
import datetime as dt
from sklearn.preprocessing import OneHotEncoder

def convertOpenTimeStamp(date_string):
    dt_obj = dt.datetime.strptime(date_string,
                            '%Y-%m-%d %H:%M:%S')
    millisec = dt_obj.timestamp() * 1000
    return int(millisec)

def convertCloseTimeStamp(date_string):
    dt_obj = dt.datetime.strptime(date_string,
                            '%Y-%m-%d %H:%M:%S.%f')
    millisec = dt_obj.timestamp() * 1000
    return int(millisec)

df = pd.read_csv("Price_Data/BTCUSDT_Data.csv")
df = df.set_index('Index')

del df["O"]


# for i in range(len(df)):
#     df.loc[i, 'Open_Time'] = convertOpenTimeStamp(df.loc[i, 'Open_Time'])
    
# for i in range(len(df)):
#     df.loc[i, 'Close_Time'] = convertCloseTimeStamp(df.loc[i, 'Close_Time'])
        
dataset = df["C"]
df = df.rename(columns={'C': 'now'})
dataset = dataset.to_list()
dataset = dataset[1:]
df = df[:-1]
df.insert(3, "Future", dataset)



df.to_csv("Price_Data/Rendered_Data_4h.csv")