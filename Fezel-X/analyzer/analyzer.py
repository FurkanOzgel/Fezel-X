import json
import pandas as pd

def analyse_cari_oran(data):

    deviation_percentage = data.config["cari_oran_deviation_percentage"]
    cari_oran_list = json.loads(data.ratios.iloc[0]["Cari_Oran"])

    # Step-1 Start
    if cari_oran_list[0] > 1:
        print("up")

    # Step-1 End

    # Step-2 Start
    if 1.5 < cari_oran_list[0] < 2.5:
        print("up")

    if cari_oran_list[0] > 2.5:
        # 2.5 la 8 arasındaki fark yüzde kaç

        # 6.5 2.5'un yüzde kaçı bu yüzdde sapmadan büyükse no proble but değilse down
        if (cari_oran_list[0] - 2.5):
            pass

    # Step-2 End

    # Step-3 Start
    # print(data.sector_average_ratios.iloc[0]["Cari_Oran"])
    # print(json.loads(data.ratios.iloc[0]["Cari_Oran"]))
    # Step-3 End
    

class Analyzer:
    def __init__(self, config):
        self.config = config
        self.shareName = config["share_name"]

        share_sector_df = pd.read_csv("data/share_sector_df.csv", index_col=0)
        sector = share_sector_df[share_sector_df["Share"] == self.shareName].iloc[0]["Sector"]

        share_ratio_df = pd.read_csv("data/share_ratio_df.csv", index_col=0)
        self.ratios = share_ratio_df[share_ratio_df["Share_Name"] == self.shareName]

        sector_average_df = pd.read_csv("data/sector_average_df.csv", index_col=0)
        self.sector_average_ratios = sector_average_df[sector_average_df["Sector"] == sector]
        
        self.point_df = pd.read_csv("data/point_df.csv", index_col=0)

    def produce_empty_point_df():
        df = pd.read_csv("data/share_ratio_df.csv", index_col=0)
        columns_to_zero = df.columns.difference(['Share_Name'])  

        df[columns_to_zero] = 0
        
        df.to_csv("data/emty_point_df.csv")

    def initilaze(self):
        analyse_cari_oran(self)
        
