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
    cari_oran_point = 0
    point_list = data.config["cari_oran_rating"]
    deviation_percentage = data.config["cari_oran_deviation_percentage"]
    cari_oran_list = json.loads(data.ratios.iloc[0]["Cari_Oran"])
    
    print(f"\n\033[1mCari Oran: {cari_oran_list[0]}\033[0m")

    # Step-1.1 Start
    if cari_oran_list[0] > 1:
        print("\nStep-1.1: up")
        cari_oran_point = cari_oran_point + point_list[0]
    else:
        print("\nStep-1.1: down")
        cari_oran_point = cari_oran_point + point_list[1]
    # Step-1.1 End

    # Step-1.2 Start
    max_deviation_value = 2.5 + (1.75 * deviation_percentage / 100)
    min_deviation_value = 1.5 - (1.75 * deviation_percentage / 100)

    if 1.5 < cari_oran_list[0] < 2.5:
        print("Step-1.2: up")
        cari_oran_point = cari_oran_point + point_list[2]
    elif max_deviation_value < cari_oran_list[0]:
        print("Step-1.2: nötr")
        cari_oran_point = cari_oran_point + point_list[3]
    elif min_deviation_value > cari_oran_list[0]:
        print("Step-1.2: nötr")
        cari_oran_point = cari_oran_point + point_list[4]
    else:
        print("Step-1.2: down ")
        cari_oran_point = cari_oran_point + point_list[5]

    # Step-1.2 End

    # Step-1.3 Start
    sector_average = data.sector_average_ratios.iloc[0]["Cari_Oran"]

    if cari_oran_list[0] > sector_average:
        print("Step-1.3: up")
        cari_oran_point = cari_oran_point + point_list[6]
    else:
        print("Step-1.3: down")
        cari_oran_point = cari_oran_point + point_list[7]

    # Step-1.3 End

    # Step-1.4 Start
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
            cari_oran_point = cari_oran_point + point_list[8]
        else:
            print("Step-1.4: down")
            cari_oran_point = cari_oran_point + point_list[9]


    elif trend_list[-1][0] == "bear":
        if trend_list[-1][1][-1] < trend_list[-1][1][-2]:
            print("Step-1.4: nötr")
            cari_oran_point = cari_oran_point + point_list[10]
        else:
            print("Step-1.4: up")
            cari_oran_point = cari_oran_point + point_list[11]

    # Step-1.4 End

    print(f"\n\033[1mCari Oran Puanı: {cari_oran_point}\033[0m")
    print("=" * 50)

def analyse_nakit_oran(data):
    nakit_oran_point = 0
    point_list = data.config["nakit_oran_rating"]
    nakit_oran = json.loads(data.ratios.iloc[0]["Nakit_Oran"])[0]

    print(f"\n\033[1mNakit Oran: {nakit_oran}\033[0m")
    print()

    # Step-2.1 Start
    if 0.18 > nakit_oran > 0.22:
        print("Step-2.1: up")
        nakit_oran_point = nakit_oran_point + point_list[0]
    elif 0.22 < nakit_oran:
        print("Step-2.1: down")
        nakit_oran_point = nakit_oran_point + point_list[1]
    elif 0.18 > nakit_oran:
        print("Step-2.1: down")
        nakit_oran_point = nakit_oran_point + point_list[2]
    # Step-2.1 End

    print(f"\n\033[1mNakit Oran Puanı: {nakit_oran_point}\033[0m")
    print("=" * 50)

def analyse_yabancı_kaynak_ozkaynak(data):
    yabancı_kaynak_ozkaynak_point = 0
    point_list = data.config["yabancı_kaynak_ozkaynak_rating"]
    yabancı_kaynak_ozkaynak = json.loads(data.ratios.iloc[0]["Toplam_Yabancı_Kaynaklar_Oz_Kaynaklar_Oranı"])[0]

    print(f"\n\033[1mToplam Yabancı Kaynaklar / Öz Kaynaklar: {yabancı_kaynak_ozkaynak}\033[0m")
    print()

    # Step-3.1 Start
    if 0 < yabancı_kaynak_ozkaynak < 0.5:
        print("Step-3.1: nötr")
        yabancı_kaynak_ozkaynak_point = yabancı_kaynak_ozkaynak_point + point_list[0]

    elif 0.5 < yabancı_kaynak_ozkaynak < 1:
        print("Step-3.1: nötr")
        yabancı_kaynak_ozkaynak_point = yabancı_kaynak_ozkaynak_point + point_list[1]

    elif 1 < yabancı_kaynak_ozkaynak < 2:
        print("Step-3.1: nötr")
        yabancı_kaynak_ozkaynak_point = yabancı_kaynak_ozkaynak_point + point_list[2]
    
    else:
        print("Step-3.1: nötr")
        yabancı_kaynak_ozkaynak_point = yabancı_kaynak_ozkaynak_point + point_list[3]
    # Step-3.1 End

    print(f"\n\033[1mToplam Yabancı Kaynaklar / Öz Kaynaklar Puanı: {yabancı_kaynak_ozkaynak_point}\033[0m")
    print("=" * 50)

def analyse_alacak_devir_hızı(data):
    alacak_devir_hızı_point = 0
    point_list = data.config["alacak_devir_hızı_rating"]
    deviation_percentage = data.config["devir_hızı_deviation_percentage"]
    alacak_devir_hızı = data.ratios.iloc[0]["Alacak_Devir_Hızı"]
    sector_average = data.sector_average_ratios.iloc[0]["Alacak_Devir_Hızı"]

    print(f"\n\033[1mAlacak Devir Hızı: {alacak_devir_hızı}\033[0m")
    print()

    if sector_average * (1 + deviation_percentage) < alacak_devir_hızı:
        print("Step-4.1: up")
        alacak_devir_hızı_point = alacak_devir_hızı_point + point_list[0]
    elif sector_average * (1 - deviation_percentage) < alacak_devir_hızı:
        print("Step-4.1: down")
        alacak_devir_hızı_point = alacak_devir_hızı_point + point_list[1]
    else:
        print("Step-4.1: nötr")
        alacak_devir_hızı_point = alacak_devir_hızı_point + point_list[2]

    print(f"\n\033[1mAlacak Devir Hızı Puanı: {alacak_devir_hızı_point}\033[0m")
    print("=" * 50)

def analyse_aktif_devir_hızı(data):
    aktif_devir_hızı_point = 0
    point_list = data.config["aktif_devir_hızı_rating"]
    deviation_percentage = data.config["devir_hızı_deviation_percentage"]
    aktif_devir_hızı = data.ratios.iloc[0]["Aktif_Devir_Hızı"]
    sector_average = data.sector_average_ratios.iloc[0]["Aktif_Devir_Hızı"]

    print(f"\n\033[1mAktif Devir Hızı: {aktif_devir_hızı}\033[0m")
    print()

    if sector_average * (1 + deviation_percentage) < aktif_devir_hızı:
        print("Step-5.1: up")
        aktif_devir_hızı_point = aktif_devir_hızı_point + point_list[0]
    elif sector_average * (1 - deviation_percentage) < aktif_devir_hızı:
        print("Step-5.1: down")
        aktif_devir_hızı_point = aktif_devir_hızı_point + point_list[1]
    else:
        print("Step-5.1: nötr")
        aktif_devir_hızı_point = aktif_devir_hızı_point + point_list[2]

    print(f"\n\033[1mAktif Devir Hızı Puanı: {aktif_devir_hızı_point}\033[0m")
    print("=" * 50)

def analyse_ozvarlık_karlıgı(data):
    ozvarlık_karlıgı_point = 0
    point_list = data.config["ozvarlık_karlıgı_rating"]
    deviation_percentage = data.config["oz_varlık_deviation_percentage"]
    ozvarlık_karlıgı_list = eval(data.ratios.iloc[0]["Oz_Varlık_Karlılıgı"])
    ozvarlık_karlıgı = float(ozvarlık_karlıgı_list[0])
    sector_average = data.sector_average_ratios.iloc[0]["Oz_Varlık_Karlılıgı"]

    print(f"\n\033[1mÖz Varlık Kârlılığı: {ozvarlık_karlıgı_list[0]}\033[0m")
    print()

    if sector_average * (1 + deviation_percentage) < ozvarlık_karlıgı:
        print("Step-6.1: up")
        ozvarlık_karlıgı_point = ozvarlık_karlıgı_point + point_list[0]
    elif sector_average * (1 - deviation_percentage) < ozvarlık_karlıgı:
        print("Step-6.1: down")
        ozvarlık_karlıgı_point = ozvarlık_karlıgı_point + point_list[1]
    else:
        print("Step-6.1: nötr")
        ozvarlık_karlıgı_point = ozvarlık_karlıgı_point + point_list[2]

    try:
        if ozvarlık_karlıgı_list[0] > ozvarlık_karlıgı_list[3]:
            print("Step-6.2: up")
            ozvarlık_karlıgı_point = ozvarlık_karlıgı_point + point_list[3]
        else:
            print("Step-6.2: down")
            ozvarlık_karlıgı_point = ozvarlık_karlıgı_point + point_list[4]
    except:
        pass

    print(f"\n\033[1mÖz Varlık Kârlılığı Puanı: {ozvarlık_karlıgı_point}\033[0m")
    print("=" * 50)

def analyse_kar_marjları(data):
    kar_marjları_point = 0
    point_list = data.config["kar_marjları_rating"]
    deviation_percentage = data.config["kar_marjları_deviation_percentage"]
    kar_marjları_list = eval(data.ratios.iloc[0]["Kar_Marjları"])
    sector_average = eval(data.sector_average_ratios.iloc[0]["Kar_Marjları"])

    print(f"\n\033[1mKâr Marjları:\033[0m")
    for key, value in kar_marjları_list.items():
        print(f"   {key}: \033[1m{value[0]}\033[0m")
    print()

    for key, value in kar_marjları_list.items():
        if float(sector_average[key]) * (1 + deviation_percentage) < float(value[0]):
            print("Step-7.1: up")
            kar_marjları_point = kar_marjları_point + point_list[0]
        elif float(sector_average[key]) * (1 - deviation_percentage) < float(value[0]):
            print("Step-7.1: down")
            kar_marjları_point = kar_marjları_point + point_list[1]
        else:
            print("Step-7.1: nötr")
            kar_marjları_point = kar_marjları_point + point_list[2]

        try:
            if float(value[0]) > float(value[3]):
                print("Step-7.2: up")
                kar_marjları_point = kar_marjları_point + point_list[3]
            else:
                print("Step-7.2: down")
                kar_marjları_point = kar_marjları_point + point_list[4]
        except:
            pass

        print()
    
    print(f"\n\033[1mKâr Marjları: Puanı: {kar_marjları_point}\033[0m")
    print("=" * 50)

def analyse_hbk(data):
    hbk_point = 0
    point_list = data.config["hbk_rating"]
    hbk_list = eval(data.ratios.iloc[0]["Hisse_Bası_Kazanc"])
    hbk = float(hbk_list[0])

    try:
        print(f"\n\033[1mHisse Başı Kazanç: {hbk_list[0]}\033[0m")
        print()

        if hbk_list[0] > hbk_list[2]:
            print("Step-8.1: up")
            hbk_point = hbk_point + point_list[0]
        else:
            print("Step-8.1: down")
            hbk_point = hbk_point + point_list[1]

        print(f"\n\033[1mHisse Başı Kazanç Puanı: {hbk_point}\033[0m")
    except:
        print("!!!HBK ERROR!!!")
    
    print("=" * 50)


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
        analyse_nakit_oran(self)
        analyse_yabancı_kaynak_ozkaynak(self)
        analyse_alacak_devir_hızı(self)
        analyse_aktif_devir_hızı(self)
        analyse_ozvarlık_karlıgı(self)
        analyse_kar_marjları(self)
        analyse_hbk(self)
        
