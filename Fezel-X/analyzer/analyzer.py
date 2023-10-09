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
    cari_oran_list = cari_oran_list[:] 
    cari_oran_list.reverse()

    trend_list = []

    stop_trend_search_loop = False

    while not stop_trend_search_loop:

        stop_trend_search_loop = True

        min_value_trend = (float('inf'), 0)
        max_value_trend = (0, 0)
        finish_index = len(cari_oran_list)

        trend_percentage = data.config['cari_oran_percentage_change_for_the_trend']

        temporary_data = []

        for value in cari_oran_list[:]:
            if value < min_value_trend[0]:
                min_value_trend = (value, cari_oran_list.index(value))
            
            if value > max_value_trend[0]:
                max_value_trend = (value, cari_oran_list.index(value))
            
            if max_value_trend[0] > min_value_trend[0] * (1 + trend_percentage) and max_value_trend[1] > min_value_trend[1]:
                min_value_trend = (float('inf'), 0)
                max_value_trend = (0, 0)

                temporary_data = cari_oran_list[min_value_trend[1]+1:]

                for value in temporary_data:
                    if value < min_value_trend[0]:
                        min_value_trend = (value, cari_oran_list.index(value))
                    
                    if value > max_value_trend[0]:
                        max_value_trend = (value, cari_oran_list.index(value))
        
                    if max_value_trend[0] * (1 - trend_percentage) > min_value_trend[0] and max_value_trend[1] < min_value_trend[1]:   
                        finish_index = max_value_trend[1] + 1
                        break
                
                trend_list.append(("bull" ,cari_oran_list[:finish_index]))
                cari_oran_list = cari_oran_list[finish_index-1:]
                stop_trend_search_loop = False
                break

            elif max_value_trend[0] * (1 - trend_percentage) > min_value_trend[0] and max_value_trend[1] < min_value_trend[1]:
                min_value_trend = (float('inf'), 0)
                max_value_trend = (0, 0)

                temporary_data = cari_oran_list[max_value_trend[1]+1:]

                for value in temporary_data:
                    if value < min_value_trend[0]:
                        min_value_trend = (value, cari_oran_list.index(value))
                    
                    if value > max_value_trend[0]:
                        max_value_trend = (value, cari_oran_list.index(value))

                    if max_value_trend[0] > min_value_trend[0] * (1 + trend_percentage) and max_value_trend[1] > min_value_trend[1]:
                        finish_index = min_value_trend[1] + 1
                        break
                
                trend_list.append(("bear", cari_oran_list[:finish_index]))
                cari_oran_list = cari_oran_list[finish_index-1:]
                stop_trend_search_loop = False
                break
    
    if trend_list[-1][0] == "bull":
        if trend_list[-1][1][-1] > trend_list[-1][1][-2]:
            print("Step-1.4: nötr")
        else:
            print("Step-1.4: down")

    elif trend_list[-1][0] == "bear":
        if trend_list[-1][1][-1] < trend_list[-1][1][-2]:
            print("Step-1.4: nötr")
        else:
            print("Step-1.4: up")

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
        
