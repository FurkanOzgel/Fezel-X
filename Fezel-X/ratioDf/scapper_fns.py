import requests
import os

import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import numpy as np
import time
from selenium import webdriver
import unicodedata
import datetime

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

def run_downloader_driver(path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": path
    })

    global driver
    driver = webdriver.Chrome(options=chrome_options)
        
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
    
def get_historical_financal_tables(share_name, dateIndex):
    
    firs_table_items = np.array([0 ,0 ,0 ,0])
    second_table_items = np.array([0 ,0 ,0 ,0])
    third_table_items = np.array([0 ,0 ,0 ,0])
    table_items = []
    table_item_codes = []
    sheet_date = get_sheet_dates(share_name)
    columns = ["ItemCode"] + sheet_date[dateIndex: dateIndex + 12]

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
        ("year1", sheet_date[dateIndex].split("/")[0]),
        ("period1", sheet_date[dateIndex].split("/")[1]),
        ("year2", sheet_date[dateIndex + 1].split("/")[0]),
        ("period2", sheet_date[dateIndex + 1].split("/")[1]),
        ("year3", sheet_date[dateIndex + 2].split("/")[0]),
        ("period3", sheet_date[dateIndex + 2].split("/")[1]),
        ("year4", sheet_date[dateIndex + 3].split("/")[0]),
        ("period4", sheet_date[dateIndex + 3].split("/")[1]),
        ),
        (
        ("companyCode", share_name),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", sheet_date[dateIndex + 4].split("/")[0]),
        ("period1", sheet_date[dateIndex + 4].split("/")[1]),
        ("year2", sheet_date[dateIndex + 5].split("/")[0]),
        ("period2", sheet_date[dateIndex + 5].split("/")[1]),
        ("year3", sheet_date[dateIndex + 6].split("/")[0]),
        ("period3", sheet_date[dateIndex + 6].split("/")[1]),
        ("year4", sheet_date[dateIndex + 7].split("/")[0]),
        ("period4", sheet_date[dateIndex + 7].split("/")[1]),
        ),
        (
        ("companyCode", share_name),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", sheet_date[dateIndex + 8].split("/")[0]),
        ("period1", sheet_date[dateIndex + 8].split("/")[1]),
        ("year2", sheet_date[dateIndex + 9].split("/")[0]),
        ("period2", sheet_date[dateIndex + 9].split("/")[1]),
        ("year3", sheet_date[dateIndex + 10].split("/")[0]),
        ("period3", sheet_date[dateIndex + 10].split("/")[1]),
        ("year4", sheet_date[dateIndex + 11].split("/")[0]),
        ("period4", sheet_date[dateIndex + 11].split("/")[1]),
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

def get_ready_historical_ratio_tradingview(path, dateIndex):
    
    element = driver.find_elements("xpath",path)[0]

    child_elements = element.find_elements("xpath", "./*")
    child_texts = [remove_unicode_control_characters(child.text) for child in child_elements]

    return list(reversed(child_texts))[dateIndex + 1:]

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

def get_historical_hbk(share_name, date):
    url = f"https://tr.tradingview.com/symbols/BIST-{share_name}/financials-income-statement/earnings-per-share-basic/"

    driver.get(url)

    time.sleep(4)

    last_sheet_year = int(datetime.datetime.now().year) - 1

    date_year = int(date.split("/")[0])

    date_difference = last_sheet_year - date_year

    
    def text_returner(element):
        return element.text

    historical_hbk = driver.find_elements("xpath", "//div[@class='item-CbBHHTvu']/div[2]")
    
    historical_hbk = list(map(text_returner, historical_hbk))
    
    if date_year > last_sheet_year:
        historical_hbk = list(map(remove_unicode_control_characters, historical_hbk))[2: 5]
    elif date_year == last_sheet_year:
        historical_hbk = list(map(remove_unicode_control_characters, historical_hbk))[3: 6]
    else:
        historical_hbk = list(map(remove_unicode_control_characters, historical_hbk))[3 + date_difference: 9]



    return historical_hbk

def get_historical_fko_with_date(share_name, date):
    url = f"https://tr.tradingview.com/symbols/BIST-{share_name}/financials-statistics-and-ratios/price-earnings/"

    driver.get(url)

    time.sleep(6)
    
    def text_returner(element):
        return element.text

    xpath_div_order = get_sheet_dates(share_name).index(date) + 2

    historical_fko = driver.find_elements("xpath", f"//*[@id='js-category-content']/div[2]/div/div[2]/div[6]/div[{xpath_div_order}]/div[2]")
    
    historical_fko = list(map(text_returner, historical_fko))
    
    historical_fko = list(map(remove_unicode_control_characters, historical_fko))

    return historical_fko[0]

def get_increase_value(share_name, date):
    file_list = os.listdir("data/report_date")

    def get_date_from_file_name(file_name):
        date_field = file_name.split('.')[0]  # Dosya adından tarih kısmını al
        return date_field

    sorted_file_list = sorted(file_list, key=get_date_from_file_name)

    if sorted_file_list[-1].split(".")[0] == date:
        raise BaseException("The date is the same as the last balance sheet date.")
    
    if date + ".csv" not in file_list:
        raise BaseException("Invalid Date")

    date_index = sorted_file_list.index(date+".csv")
    interval = [sorted_file_list[date_index], sorted_file_list[date_index+1]]

    df = pd.read_csv(f"data/report_date/{interval[0]}")
    start_df = df[df['Share'] == share_name]

    df = pd.read_csv(f"data/report_date/{interval[1]}")
    end_df = df[df['Share'] == share_name]

    detailed_interval = [start_df["Report_Date"].values[0].split(" ")[0], end_df["Report_Date"].values[0].split(" ")[0]]

    start_date = datetime.datetime.strptime(detailed_interval[0], '%Y-%m-%d')
    start_date = str(int(datetime.datetime.timestamp(start_date)))

    end_date = datetime.datetime.strptime(detailed_interval[1], '%Y-%m-%d')
    end_date = str(int(datetime.datetime.timestamp(end_date)))

    url = f"https://query1.finance.yahoo.com/v7/finance/download/{share_name}.IS?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true"

    try:
        run_downloader_driver(f"/home/furkanozgel/Desktop/Fezel-X/data/{date}/historical_price")

        driver.get(url)

        time.sleep(2)

        price_df = pd.read_csv(f"data/{date}/historical_price/{share_name}.IS.csv")

        change_percentage = (100 * price_df.iloc[-1]["Close"] / price_df.iloc[0]["Open"]) - 100
        
        return change_percentage

    except:
        return 'NaN'
