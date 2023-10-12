import os
import pandas as pd

def fill_point_df(date):
    date_path = date.replace("/", "-")
    file_list = os.listdir(f"data/{date_path}/historical_price")
    change = 0
    data = []

    for share in file_list:
        df = pd.read_csv(f"data/{date_path}/historical_price/{share}")
        open_price = df.loc[0, "Open"]
        close_price = df.iloc[-1]['Close']

        change = (close_price * 100) / open_price - 100

        data.append([share.split(".")[0], change])

    price_increase_df = pd.DataFrame(data, columns=['Share', 'Change'])
    price_increase_df.to_csv(f"data/{date_path}/price_increase_df.csv")
        
        