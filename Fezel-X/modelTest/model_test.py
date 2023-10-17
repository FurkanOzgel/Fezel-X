import os
import pandas as pd
from analyzer import Analyzer
import sys, os
import logging
import json
import random

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def log_message_in_log(message):
    with open('data/analyze_error.log', 'r') as log_dosyasi:
        log_verileri = log_dosyasi.read()
        return message in log_verileri


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
        
def run_test(date, config):
    with open('data/test_log.json', 'r', encoding="utf-8") as file:
        id_log_list = json.load(file)

    with open("data/last_id.txt", "r") as dosya:
        id = int(dosya.read().strip())

    id = id + 1

    with open("data/last_id.txt", "w") as dosya:
        dosya.write(str(id))

    same_config = False

    for log in id_log_list:
        if log["config"] == config:
            same_config = True
            config_rate = log["succes_rate"]

    if not same_config:
        print()
        print("="*60)
        print(f"\033[1mTest {id} is Running...\033[0m")

        config["df_date"] = date
        date = date.replace("/","-")
        share_list = pd.read_csv(f"data/{date}/share_ratio_df_{date}.csv")["Share_Name"].values

        point_df = pd.read_csv(f"data/{date}/share_point_df.csv", index_col=0)

        logging.basicConfig(filename='data/analyze_error.log', level=logging.DEBUG, format='%(message)s')

        for share in share_list:
            config["share_name"] = share

            try:
                blockPrint()
                point_list = Analyzer(config).initilaze()
                enablePrint()

                total = sum(point_list)
                point_list.append(total)
                point_list.insert(0, date)
                point_list.insert(0, share)

                point_df.loc[point_df['Share_Name'] == share] = point_list

            except:
                log_message = f'Date: {date} Share: {share}'

                if not log_message_in_log(log_message):
                    logging.info(log_message)

        succes_rating_list = []

        price_increase_df = pd.read_csv(f"data/{date}/price_increase_df.csv", index_col=0)

        for index, row in point_df.iterrows():
            if row["Total"] != 0:
                real_value = price_increase_df.loc[price_increase_df['Share'] == share]["Change"].values[0]
                distance = abs(row["Total"] - real_value)
                
                succes_rating_list.append(100 - (distance*100/row["Total"]))

        succes_rate = sum(succes_rating_list) / len(succes_rating_list)

        config.pop("share_name")
        new_log = {"id":id, "config": config}
        new_log["succes_rate"] = succes_rate
        id_log_list.append(new_log)

        enablePrint()
        print(f"\n\033[1mTest {id} is Done. Succes Rate: %{succes_rate}\033[0m")
        print("="*60)
        print()

        with open('data/test_log.json', "w", encoding="utf-8") as json_file:
            json.dump(id_log_list, json_file, indent=4, ensure_ascii=False)

        point_df.to_csv(f"data/{date}/share_point_df.csv")

        return succes_rate
    else:
        print("")
        print(f"\033[1mAlready this configuration is tested. Succes rate: %{config_rate}\033[0m")
        print("")

        return config_rate

def search_config_value(date):
    rep_date = date.replace("/", "-")

    with open(f'data/{rep_date}/model_config.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    last_index = data["last_index"]
    optimum_list = data["points"]

    for index, point in enumerate(optimum_list[:]):
        
        config = {
            "cari_oran_deviation_percentage": 30,
            "devir_hızı_deviation_percentage": 0.1,
            "oz_varlık_deviation_percentage": 0.1,
            "kar_marjları_deviation_percentage": 0.1,
            "fs_deviation_percentage": 0.1,
            "cari_oran_percentage_change_for_the_trend": 0.19,
            "cari_oran_rating": optimum_list[:12],
            "nakit_oran_rating": optimum_list[12: 15],
            "yabancı_kaynak_ozkaynak_rating": optimum_list[15: 19],
            "alacak_devir_hızı_rating": optimum_list[19: 22],
            "aktif_devir_hızı_rating": optimum_list[22: 25],
            "ozvarlık_karlıgı_rating": optimum_list[25: 30],
            "kar_marjları_rating": optimum_list[30: 35],
            "hbk_rating": optimum_list[35: 37],
            "fs_rating": optimum_list[37: 40]
        }

        succes_rate = run_test(date, config)

        is_it_up = False
        counter = 0

        optimum_list[index] = point + 1

        config = {
            "cari_oran_deviation_percentage": 30,
            "devir_hızı_deviation_percentage": 0.1,
            "oz_varlık_deviation_percentage": 0.1,
            "kar_marjları_deviation_percentage": 0.1,
            "fs_deviation_percentage": 0.1,
            "cari_oran_percentage_change_for_the_trend": 0.19,
            "cari_oran_rating": optimum_list[:12],
            "nakit_oran_rating": optimum_list[12: 15],
            "yabancı_kaynak_ozkaynak_rating": optimum_list[15: 19],
            "alacak_devir_hızı_rating": optimum_list[19: 22],
            "aktif_devir_hızı_rating": optimum_list[22: 25],
            "ozvarlık_karlıgı_rating": optimum_list[25: 30],
            "kar_marjları_rating": optimum_list[30: 35],
            "hbk_rating": optimum_list[35: 37],
            "fs_rating": optimum_list[37: 40]
        }

        new_succes_rate = run_test(date, config)

        if new_succes_rate > succes_rate:
            is_it_up = True
        
        while True:

            if is_it_up:
                point = point * 1.1
                optimum_list[index] = point

                config = {
                    "cari_oran_deviation_percentage": 30,
                    "devir_hızı_deviation_percentage": 0.1,
                    "oz_varlık_deviation_percentage": 0.1,
                    "kar_marjları_deviation_percentage": 0.1,
                    "fs_deviation_percentage": 0.1,
                    "cari_oran_percentage_change_for_the_trend": 0.19,
                    "cari_oran_rating": optimum_list[:12],
                    "nakit_oran_rating": optimum_list[12: 15],
                    "yabancı_kaynak_ozkaynak_rating": optimum_list[15: 19],
                    "alacak_devir_hızı_rating": optimum_list[19: 22],
                    "aktif_devir_hızı_rating": optimum_list[22: 25],
                    "ozvarlık_karlıgı_rating": optimum_list[25: 30],
                    "kar_marjları_rating": optimum_list[30: 35],
                    "hbk_rating": optimum_list[35: 37],
                    "fs_rating": optimum_list[37: 40]
                }
                
                print()
                print(f"Ratio: {index}")
                print(f"Puan: {point} için deneniyor.")
                print(f"Counter: {counter}")
                print()

                new_succes_rate = run_test(date, config)

                if new_succes_rate > succes_rate and counter != 5:
                    counter = counter + 1
                    succes_rate = new_succes_rate
                    continue
                else:
                    counter = 0
                    optimum_list[index] = point * 10 / 11
                    json_data = {
                        "last_index": index + 1,
                        "points": optimum_list 
                    }
                    with open(f'data/{rep_date}/model_config.json', "w", encoding="utf-8") as json_file:
                        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                    break

            else:
                point = ((point*-1) * 1.1) * -1
                optimum_list[index] = point

                config = {
                    "cari_oran_deviation_percentage": 30,
                    "devir_hızı_deviation_percentage": 0.1,
                    "oz_varlık_deviation_percentage": 0.1,
                    "kar_marjları_deviation_percentage": 0.1,
                    "fs_deviation_percentage": 0.1,
                    "cari_oran_percentage_change_for_the_trend": 0.19,
                    "cari_oran_rating": optimum_list[:12],
                    "nakit_oran_rating": optimum_list[12: 15],
                    "yabancı_kaynak_ozkaynak_rating": optimum_list[15: 19],
                    "alacak_devir_hızı_rating": optimum_list[19: 22],
                    "aktif_devir_hızı_rating": optimum_list[22: 25],
                    "ozvarlık_karlıgı_rating": optimum_list[25: 30],
                    "kar_marjları_rating": optimum_list[30: 35],
                    "hbk_rating": optimum_list[35: 37],
                    "fs_rating": optimum_list[37: 40]
                }

                print()
                print(f"Ratio: {index}")
                print(f"Puan: {point} için deneniyor.")
                print(f"Counter: {counter}")
                print()
                
                new_succes_rate = run_test(date, config)

                if new_succes_rate > succes_rate and counter != 5:
                    counter = counter + 1
                    succes_rate = new_succes_rate
                    continue
                else:
                    counter = 0
                    optimum_list[index] = ((point* -1) * 10 / 11)* -1
                    json_data = {
                        "last_index": index + 1,
                        "points": optimum_list 
                    }
                    with open(f'data/{rep_date}/model_config.json', "w", encoding="utf-8") as json_file:
                        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                    break

            



