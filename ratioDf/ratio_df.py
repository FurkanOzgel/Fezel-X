import requests

import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import numpy as np
import time
from selenium import webdriver
import unicodedata
import ast

def get_sheet_dates(share_name):

    dates = []
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=" + share_name

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    choice = soup.find("select", id="ddlMaliTabloFirst")
    children = choice.findChildren("option")

    for i in children:
        dates.append(i.text)

    return dates

def remove_unicode_control_characters(text):
    cleaned_text = ""
    for char in text:
        if not unicodedata.category(char).startswith("C"):
            cleaned_text += char
    return cleaned_text

def run_driver():
    global driver
    driver = webdriver.Chrome()
    
def stop_driver():
    driver.quit()

def get_financal_tables(share_name, year, month):

    table_items = []
    table_values = []
    table_item_codes = []

    url = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"

    main_url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=" + share_name
    grup_respone = requests.get(main_url)
    soup = BeautifulSoup(grup_respone.text, "html.parser")

    choice = soup.find("select", id="ddlMaliTabloGroup")
    grup = choice.find("option")["value"]

    if (grup == "UFRS"):
        grup = "UFRS_K"

    parametreler = (
        ("companyCode", share_name),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", year),
        ("period1", month),
        ("year2", year),
        ("period2", month),
        ("year3", year),
        ("period3", month),
        ("year4", year),
        ("period4", month)
        )

    response = requests.get(url, params=parametreler).json()["value"]

    for i in response:

        table_items.append(i["itemDescTr"])
        table_values.append(i["value1"])
        table_item_codes.append(i["itemCode"])

    df = pd.DataFrame(index=table_items, columns=["ItemCode", "Values"])

    df["Values"] = table_values
    df["ItemCode"] = table_item_codes

    return df
    
def get_historical_financal_tables(share_name):
    
    firs_table_items = np.array([0 ,0 ,0 ,0])
    second_table_items = np.array([0 ,0 ,0 ,0])
    third_table_items = np.array([0 ,0 ,0 ,0])
    table_items = []
    table_item_codes = []
    sheet_date = get_sheet_dates(share_name)
    columns = ["ItemCode"] + sheet_date[:12]

    url = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
    
    main_url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=" + share_name
    grup_respone = requests.get(main_url)
    soup = BeautifulSoup(grup_respone.text, "html.parser")

    choice = soup.find("select", id="ddlMaliTabloGroup")
    grup = choice.find("option")["value"]

    if (grup == "UFRS"):
        grup = "UFRS_K"

    parametreler = [
        (
        ("companyCode", share_name),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", sheet_date[0].split("/")[0]),
        ("period1", sheet_date[0].split("/")[1]),
        ("year2", sheet_date[1].split("/")[0]),
        ("period2", sheet_date[1].split("/")[1]),
        ("year3", sheet_date[2].split("/")[0]),
        ("period3", sheet_date[2].split("/")[1]),
        ("year4", sheet_date[3].split("/")[0]),
        ("period4", sheet_date[3].split("/")[1]),
        ),
        (
        ("companyCode", share_name),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", sheet_date[4].split("/")[0]),
        ("period1", sheet_date[4].split("/")[1]),
        ("year2", sheet_date[5].split("/")[0]),
        ("period2", sheet_date[5].split("/")[1]),
        ("year3", sheet_date[6].split("/")[0]),
        ("period3", sheet_date[6].split("/")[1]),
        ("year4", sheet_date[7].split("/")[0]),
        ("period4", sheet_date[7].split("/")[1]),
        ),
        (
        ("companyCode", share_name),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", sheet_date[8].split("/")[0]),
        ("period1", sheet_date[8].split("/")[1]),
        ("year2", sheet_date[9].split("/")[0]),
        ("period2", sheet_date[9].split("/")[1]),
        ("year3", sheet_date[10].split("/")[0]),
        ("period3", sheet_date[10].split("/")[1]),
        ("year4", sheet_date[11].split("/")[0]),
        ("period4", sheet_date[11].split("/")[1]),
        )
        ]

    response = [
        requests.get(url, params=parametreler[0]).json()["value"],
        requests.get(url, params=parametreler[1]).json()["value"],
        requests.get(url, params=parametreler[2]).json()["value"]
    ]

    for i in response[0]:
        row_values = np.array([i["value1"], i["value2"], i["value3"], i["value4"]])  
        firs_table_items = np.vstack((firs_table_items, row_values))
        table_items.append(i["itemDescTr"])
        table_item_codes.append(i["itemCode"])
        
    for i in response[1]:
        row_values = np.array([i["value1"], i["value2"], i["value3"], i["value4"]])  
        second_table_items = np.vstack((second_table_items, row_values))
        
    for i in response[2]:
        row_values = np.array([i["value1"], i["value2"], i["value3"], i["value4"]])  
        third_table_items = np.vstack((third_table_items, row_values))  

    table_item_codes = np.array(table_item_codes).reshape(147, 1)

    firs_table_items = firs_table_items[1:, :]
    second_table_items = second_table_items[1:, :]
    third_table_items = third_table_items[1:, :]

    merged_np_array = np.hstack((firs_table_items, second_table_items, third_table_items))
    merged_np_array = np.concatenate((table_item_codes, merged_np_array), axis=1)

    df = pd.DataFrame(merged_np_array ,index=table_items, columns=columns)
    
    return df

def get_ready_ratio(share_name, path):
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+share_name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dom = etree.HTML(str(soup))
    
    try:
        return float(dom.xpath(path)[0].text.replace(",", "."))
    except:
        return dom.xpath(path)[0].text.replace(",", ".")

def get_ready_ratio_tradingview(share_name, path):
    url = f"https://tr.tradingview.com/symbols/{share_name}/financials-statistics-and-ratios/"

    driver.get(url)
    
    time.sleep(4)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))

    
    try:
        return float(remove_unicode_control_characters(dom.xpath(path)[0].text))
    except:
        return remove_unicode_control_characters(dom.xpath(path)[0].text)

def set_driver_for_historical(share_name):
    url = f"https://tr.tradingview.com/symbols/{share_name}/financials-statistics-and-ratios/"

    driver.get(url)
    
    time.sleep(5)

def get_ready_historical_ratio_tradingview(path):
    
    element = driver.find_elements("xpath",path)[0]

    child_elements = element.find_elements("xpath", "./*")
    child_texts = [remove_unicode_control_characters(child.text) for child in child_elements]

    return list(reversed(child_texts))

def get_ready_ratio_tradingview_summary(share_name, path):
    url = f"https://tr.tradingview.com/symbols/{share_name}/"

    driver.get(url)

    time.sleep(4)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))
    
    try:
        return float(dom.xpath(path)[0].text)
    except:
        return dom.xpath(path)[0].text

def get_ready_ratio_tradingview_test(share_name, path):
    url = f"https://tr.tradingview.com/symbols/{share_name}/financials-statistics-and-ratios/"

    driver.get(url)

    time.sleep(4)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))
    
    try:
        return float(remove_unicode_control_characters(dom.xpath(path)[0].text))
    except:
        return remove_unicode_control_characters(dom.xpath(path)[0].text)

def get_historical_hbk(share_name):
    url = f"https://tr.tradingview.com/symbols/BIST-{share_name}/financials-income-statement/earnings-per-share-basic/"

    driver.get(url)

    time.sleep(4)
    
    def text_returner(element):
        return element.text

    historical_hbk = driver.find_elements("xpath", "//div[@class='item-CbBHHTvu']/div[2]")
    
    historical_hbk = list(map(text_returner, historical_hbk))
    
    historical_hbk = list(map(remove_unicode_control_characters, historical_hbk))[1:4]

    return historical_hbk

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
       
def getData():
    
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
    
def updateData():
    print("updated df")

def update_share_sector_df():
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

def produce_sector_average_df():
    
    def first_element(lst):
        return lst[0]
    
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
        
        print(filtered_share_ratio_df["Share_Name"])

        # last_cari_oran = [print(sublist[1:-1].split(" ")[0]) for sublist in filtered_share_ratio_df["Cari_Oran"].tolist()]
        # print(last_cari_oran)
        # average_cari_oran = sum(last_cari_oran) / len(last_cari_oran)
        # df.loc[df["Sector"] == share_sector, 'Cari_Oran'] = average_cari_oran
        

        break
    
    # print(df)
