import json
import pandas as pd
import matplotlib.pyplot as plt

def produce_empty_point_df(date):
    date = date.replace("/","-")
    df = pd.read_csv(f"data/{date}/share_ratio_df_{date}.csv", index_col=0)

    df['Total'] = 0

    columns_to_zero = df.columns.difference(['Share_Name'])  
    df[columns_to_zero] = 0

    df.to_csv(f"data/{date}/share_point_df.csv")

def analyse_cari_oran(data):
    deviation_percentage = data.config["cari_oran_deviation_percentage"]
    cari_oran_list = json.loads(data.ratios.iloc[0]["Cari_Oran"])
    
    print(f"\n\033[1mCari Oran: {cari_oran_list[0]}\033[0m")

    # Step-1 Start
    if cari_oran_list[0] > 1:
        print("\nStep-1.1: up")
    else:
        print("\nStep-1.1: down")
    # Step-1 End

    # Step-2 Start
    max_deviation_value = 2.5 + (1.75 * deviation_percentage / 100)
    min_deviation_value = 1.5 - (1.75 * deviation_percentage / 100)

    if 1.5 < cari_oran_list[0] < 2.5:
        print("Step-1.2: up")
    elif max_deviation_value < cari_oran_list[0]:
        print("Step-1.2: nötr")
    elif min_deviation_value > cari_oran_list[0]:
        print("Step-1.2: nötr")
    else:
        print("Step-1.2: down ")
    # Step-2 End

    # Step-3 Start
    sector_average = data.sector_average_ratios.iloc[0]["Cari_Oran"]

    if cari_oran_list[0] > sector_average:
        print("Step-1.3: up")
    else:
        print("Step-1.3: down")
    # Step-3 End

    # Step-4 Start
    cari_oran_list_copy = cari_oran_list[:] 
    cari_oran_list_copy.reverse()

    x = list(range(len(cari_oran_list_copy)))
    plt.plot(x, cari_oran_list_copy)
    plt.show()

    print(cari_oran_list_copy)
    print(x)

    # Step-4 End

    
    print()

class Analyzer:
    def __init__(self, config):
        self.config = config
        self.shareName = config["share_name"]

        share_sector_df = pd.read_csv("data/share_sector_df.csv", index_col=0)
        sector = share_sector_df[share_sector_df["Share"] == self.shareName].iloc[0]["Sector"]

        self.date = config["df_date"].replace("/", "-")
        share_ratio_df = pd.read_csv(f"data/{self.date}/share_ratio_df_{self.date}.csv", index_col=0)
        self.ratios = share_ratio_df[share_ratio_df["Share_Name"] == self.shareName]

        sector_average_df = pd.read_csv(f"data/{self.date}/sector_average_df_{self.date}.csv", index_col=0)
        self.sector_average_ratios = sector_average_df[sector_average_df["Sector"] == sector]
        
        self.point_df = pd.read_csv(f"data/{self.date}/share_point_df.csv", index_col=0)

    def initilaze(self):
        analyse_cari_oran(self)
        
