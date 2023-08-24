import requests
import json

import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import numpy as np

from .scapper_fns import *

def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return average

class Share:
    def __init__(self, share_name):

        self.share_name = share_name
        
        self.sheetDate = get_sheet_dates(share_name)[0].split("/")

        last_year = get_sheet_dates(share_name)[4].split("/")
        self.last_year_sheet = get_financal_tables(share_name, last_year[0],
                                                        last_year[1])
        
        self.sheet = get_financal_tables(share_name, self.sheetDate[0], self.sheetDate[1])
        self.historicalSheet = get_historical_financal_tables(share_name)
        
    def cariOran(self):
        tum_donen_varlıklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '1AI'].iloc[0, 1:].tolist(), dtype=float)
        kisa_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2A'].iloc[0, 1:].tolist(), dtype=float)
        
        return np.array(tum_donen_varlıklar / kisa_vadeli_yabanci_kaynaklar).tolist()
    
    def nakitOran(self):
        nakit_nakit_benzeri = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '1AA'].iloc[0, 1:].tolist(), dtype=float)
        finansal_yatırımlar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '1AB'].iloc[0, 1:].tolist(), dtype=float)
        kisa_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2A'].iloc[0, 1:].tolist(), dtype=float)
        
        return np.array((nakit_nakit_benzeri + finansal_yatırımlar) / kisa_vadeli_yabanci_kaynaklar).tolist()
    
    def toplamYabancıKaynaklarOzKaynaklar(self):
        uzun_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2B'].iloc[0, 1:].tolist(), dtype=float)
        kisa_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2A'].iloc[0, 1:].tolist(), dtype=float)
        oz_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2N'].iloc[0, 1:].tolist(), dtype=float)
        
        return np.array((uzun_vadeli_yabanci_kaynaklar + kisa_vadeli_yabanci_kaynaklar) / oz_kaynaklar).tolist()
    
    def alacakDevirHızı(self):
        sales = float(self.sheet[self.sheet["ItemCode"] == '3C'].iloc[0, 1])

        for i, y in self.last_year_sheet.iterrows():
            if y.ItemCode == "3C":
                last_year_sales = float(y.Values)
        sales_ortalamasi = (float(sales) + last_year_sales) / 2
        
        alacaklar = float(self.sheet[self.sheet["ItemCode"] == '1AC'].iloc[0, 1])

        for i, y in self.last_year_sheet.iterrows():
            if y.ItemCode == "1AC":
                last_year_alacak = float(y.Values)
                
        alacak_ortalamasi = (alacaklar + last_year_alacak) / 2
        
        return sales_ortalamasi / alacak_ortalamasi
    
    def aktifDevirHızı(self):
        sales = float(self.sheet[self.sheet["ItemCode"] == '3C'].iloc[0, 1])
        toplam_varlıklar = float(self.sheet[self.sheet["ItemCode"] == '1BL'].iloc[0, 1])
        
        return sales/toplam_varlıklar
    
    def karMarjları(self):        
        varlık_getirisi = get_ready_historical_ratio_tradingview("//*[@id='js-category-content']/div[2]/div/div/div[6]/div[2]/div/div[1]/div[12]/div[5]")
        yatırılan_sermayenin_getirisi = get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[14]/div[5]')
        brüt_kar_marjı = get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[15]/div[5]')
        faliyet_kar_marjı = get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]')
        favök_marjı = get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[17]/div[5]')
        net_marj = get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[18]/div[5]')
        
        return {
            "varlık_getirisi": varlık_getirisi,
            "yatırılan_sermayenin_getirisi": yatırılan_sermayenin_getirisi, 
            "brüt_kar_marjı": brüt_kar_marjı, 
            "faliyet_kar_marjı": faliyet_kar_marjı, 
            "favök_marjı": favök_marjı, 
            "net_marj": net_marj
            }
    
    def ozvarlıkKarlılıgı(self):
        set_driver_for_historical(self.share_name)
        
        return get_ready_historical_ratio_tradingview( "//*[@id='js-category-content']/div[2]/div/div/div[6]/div[2]/div/div[1]/div[13]/div[5]")
    
    def hisseBasıKazanc(self):
        return get_historical_hbk(self.share_name)
    
    def fiyatSatısOranı(self):
        fiyat_kazanc = get_ready_ratio_tradingview_summary(f"BIST-{self.share_name}", "//*[@id='js-category-content']/div[2]/div/section/div[2]/div[2]/div[3]/div[2]/div[1]")
        
        return fiyat_kazanc

def create_share_ratio_df():
    share_sector_df = pd.read_csv("data/share_sector_df.csv", index_col=0)

    columns = ["Share_Name", "Bilanco_Date", "Cari_Oran", "Nakit_Oran", "Toplam_Yabancı_Kaynaklar_Oz_Kaynaklar_Oranı",
                "Alacak_Devir_Hızı", "Aktif_Devir_Hızı", "Oz_Varlık_Karlılıgı", "Kar_Marjları", "Hisse_Bası_Kazanc",
                "Fiyat_Satıs_Oranı"]
    
    try:
        share_ratio_df = pd.read_csv("data/share_ratio_df.csv", index_col=0)
    except:
        share_ratio_df = pd.DataFrame(columns=columns)
        
    with open("data/faulty_shares.txt", "r", encoding="UTF-8") as file:
        mistake_count = len(file.readlines()) - 1
        
        if mistake_count == -1:
            mistake_count = 0
    
    start_index = share_ratio_df.shape[0] + mistake_count
    
    run_driver()

    for index, row in share_sector_df[start_index:].iterrows():
        
        with open("config/loop_stopper.txt", "r", encoding="UTF-8") as file:
            runLoop = file.read()
                
        try:
            if runLoop == "0":
                raise Exception("You Stopped Loop")
            
            if("," in row["Share"]):
                raise Exception("Invalid share")
            
            share = Share(row["Share"])
            
            share_name = share.share_name
            bilanco_date = share.sheetDate[0] + "/" +share.sheetDate[1]
            cari_oran = share.cariOran()
            nakit_oran = share.nakitOran()
            toplam_yabancı_kaynaklar_oz_kaynaklar = share.toplamYabancıKaynaklarOzKaynaklar()
            alacak_devir_hızı = share.alacakDevirHızı()
            aktif_devir_hızı = share.aktifDevirHızı()
            oz_varlık_karlılıgı = share.ozvarlıkKarlılıgı()
            kar_marjları = share.karMarjları()
            hisse_bası_kazanc = share.hisseBasıKazanc()
            fiyat_satıs_oranı = share.fiyatSatısOranı()

            new_row = {
                    "Share_Name": share_name, "Bilanco_Date": bilanco_date, "Cari_Oran": cari_oran,
                    "Nakit_Oran": nakit_oran, "Toplam_Yabancı_Kaynaklar_Oz_Kaynaklar_Oranı": toplam_yabancı_kaynaklar_oz_kaynaklar,
                    "Alacak_Devir_Hızı": alacak_devir_hızı, "Aktif_Devir_Hızı": aktif_devir_hızı,
                    "Oz_Varlık_Karlılıgı": oz_varlık_karlılıgı, "Kar_Marjları": kar_marjları, 
                    "Hisse_Bası_Kazanc": hisse_bası_kazanc, "Fiyat_Satıs_Oranı": fiyat_satıs_oranı
                    }
            
            share_ratio_df.loc[len(share_ratio_df)] = new_row 

            share_ratio_df.to_csv("data/share_ratio_df.csv")
            
            print("")
            print(f"{share.share_name} Scarapping Done")
            
        except Exception as e:
            print("")
            print("!!!"+row["Share"]+"!!!:")
            print(e)

            if runLoop == "0":
                break
            else:
                with open("data/faulty_shares.txt", "a", encoding="UTF-8") as file:
                    file.write(row["Share"] + "\n")

    stop_driver()

    share_ratio_df.to_csv("data/share_ratio_df.csv")
    
def update_share_ratio_df():
    print("updated df")

def create_share_sector_df():
    url = "https://www.kap.org.tr/tr/bist-sirketler"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    symbols = soup.findAll('div', class_='_04')
    df = pd.DataFrame(columns=["Share", "Sector"])
    i = 0

    for symbol in symbols:
        i = i + 1

        print(i)

        try:
            for a_tag in symbol.find_all("a"):
                res = requests.get("https://www.kap.org.tr/" + a_tag["href"]).text
                soup = BeautifulSoup(res, 'html.parser')
                dom = etree.HTML(str(soup))
                sector = dom.xpath("/html/body/div[7]/div/div/div[2]/div/div[1]/ \
                    div[7]/div[2]")[0].text.lstrip().rstrip()
                newRow = {"Share": symbol.text[1:-1], "Sector": sector}
                print(newRow)

                df = df._append(newRow, ignore_index=True)
        except IndexError:
            continue

    print(df)

    df.to_csv("data/share_sector_df.csv")

def update_share_sector_df():
    pass

def produce_sector_average_df():
    share_sector_df = pd.read_csv("data/share_sector_df.csv", index_col=0)
    share_ratio_df = pd.read_csv("data/share_ratio_df.csv", index_col=0)

    sector_list = share_sector_df["Sector"].unique()

    columns = ["Sector", "Cari_Oran", "Alacak_Devir_Hızı", "Aktif_Devir_Hızı", "Oz_Varlık_Karlılıgı", "Kar_Marjları", "Fiyat_Satıs_Oranı"]
    df = pd.DataFrame(columns=columns)
    
    df["Sector"] = sector_list
    
    for index, row in df.iterrows():
        
        share_sector = row["Sector"]
        
        filtered_share_sector_df = share_sector_df[share_sector_df['Sector'] == share_sector]
        share_name_list = filtered_share_sector_df["Share"].tolist()
        
        filtered_share_ratio_df = share_ratio_df[share_ratio_df["Share_Name"].isin(share_name_list)]
        
        try:
            ratio_list = []
            
            for sublist in filtered_share_ratio_df['Cari_Oran'].tolist():
                try:
                    ratio_list.append(float(sublist.split(",")[0][1:]))
                except:
                    continue

            
            average = sum(ratio_list) / len(ratio_list)
            df.loc[df["Sector"] == share_sector, 'Cari_Oran'] = average
        except:
            pass
        
        try:
            ratio_list = filtered_share_ratio_df["Alacak_Devir_Hızı"].tolist()
            average = sum(ratio_list) / len(ratio_list)
            df.loc[df["Sector"] == share_sector, 'Alacak_Devir_Hızı'] = average
        except:
            pass
        
        try:
            ratio_list = filtered_share_ratio_df["Aktif_Devir_Hızı"].tolist()
            average = sum(ratio_list) / len(ratio_list)
            df.loc[df["Sector"] == share_sector, 'Aktif_Devir_Hızı'] = average
        except:
            pass
        
        try:
            ratio_list = []
            
            for sublist in filtered_share_ratio_df['Oz_Varlık_Karlılıgı'].tolist():
                try:
                    ratio_list.append(float(sublist.split(",")[0][1:].replace("−", "-").replace("'", "")))
                except:
                    continue

            average = sum(ratio_list) / len(ratio_list)
            df.loc[df["Sector"] == share_sector, 'Oz_Varlık_Karlılıgı'] = average

        except Exception as e:
            print(e)

        try:
            ratio_list = []
            
            for i in filtered_share_ratio_df['Fiyat_Satıs_Oranı'].tolist():
                try:
                    ratio_list.append(float(i))
                except:
                    continue
            average = sum(ratio_list) / len(ratio_list)
            df.loc[df["Sector"] == share_sector, 'Fiyat_Satıs_Oranı'] = average
        except:
            pass
        
        try:
            ratio_list = []
            
            json_list = [json.loads(i.replace("'", '"').replace("−", "-")) for i in filtered_share_ratio_df['Kar_Marjları'].tolist()]
            
            average_object = {
                    'varlık_getirisi':[],
                    'yatırılan_sermayenin_getirisi':[],
                    'brüt_kar_marjı':[],
                    'faliyet_kar_marjı':[],
                    'favök_marjı':[],
                    'net_marj':[]
                }
            
            for i in json_list:
                
                try:
                    average_object["varlık_getirisi"].append(float(i['varlık_getirisi'][0]))
                except:
                    pass
                
                try:
                    average_object["yatırılan_sermayenin_getirisi"].append(float(i['yatırılan_sermayenin_getirisi'][0]))
                except:
                    pass
                
                try:
                    average_object["brüt_kar_marjı"].append(float(i['brüt_kar_marjı'][0]))
                except:
                    pass
                
                try:
                    average_object["faliyet_kar_marjı"].append(float(i['faliyet_kar_marjı'][0]))
                except:
                    pass
                
                try:
                    average_object["net_marj"].append(float(i['net_marj'][0]))
                except:
                    pass
                
                try:
                    average_object["favök_marjı"].append(float(i['favök_marjı'][0]))
                except:
                    pass
                
            average_object["varlık_getirisi"] = calculate_average(average_object["varlık_getirisi"])
            average_object["yatırılan_sermayenin_getirisi"] = calculate_average(average_object["yatırılan_sermayenin_getirisi"])
            average_object["brüt_kar_marjı"] = calculate_average(average_object["brüt_kar_marjı"])
            average_object["faliyet_kar_marjı"] = calculate_average(average_object["faliyet_kar_marjı"])
            average_object["favök_marjı"] = calculate_average(average_object["favök_marjı"])
            average_object["net_marj"] = calculate_average(average_object["net_marj"])
            
            df.loc[df["Sector"] == share_sector, 'Kar_Marjları'] = json.dumps(average_object, ensure_ascii=False)
 
        except Exception as e:
            print(e)
            
    df.to_csv("data/sector_average_df.csv")
