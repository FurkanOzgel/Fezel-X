import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
from selenium import webdriver
import time
import unicodedata
import numpy as np

def run_driver():
    global driver
    driver = webdriver.Chrome()


def remove_unicode_control_characters(text):
    cleaned_text = ""
    for char in text:
        if not unicodedata.category(char).startswith("C"):
            cleaned_text += char
    return cleaned_text


def get_finance_data_dates(stock):

    dates = []
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=" + stock

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    choice = soup.find("select", id="ddlMaliTabloFirst")
    children = choice.findChildren("option")

    for i in children:
        dates.append(i.text)

    return dates


def get_financal_tables(stock, year, month):

    table_items = []
    table_values = []
    table_item_codes = []

    url = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"

    main_url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=" + stock
    grup_respone = requests.get(main_url)
    soup = BeautifulSoup(grup_respone.text, "html.parser")

    choice = soup.find("select", id="ddlMaliTabloGroup")
    grup = choice.find("option")["value"]

    if (grup == "UFRS"):
        grup = "UFRS_K"

    parametreler = (
        ("companyCode", stock),
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


def get_historical_financal_tables(stock):
    stock = "odas"
    firs_table_items = np.array([0 ,0 ,0 ,0])
    second_table_items = np.array([0 ,0 ,0 ,0])
    third_table_items = np.array([0 ,0 ,0 ,0])
    table_items = []
    table_item_codes = []
    columns = ["ItemCode"] + get_finance_data_dates(stock)[:12]

    url = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"

    main_url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=" + stock
    grup_respone = requests.get(main_url)
    soup = BeautifulSoup(grup_respone.text, "html.parser")

    choice = soup.find("select", id="ddlMaliTabloGroup")
    grup = choice.find("option")["value"]

    if (grup == "UFRS"):
        grup = "UFRS_K"

    parametreler = [
        (
        ("companyCode", stock),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", get_finance_data_dates(stock)[0].split("/")[0]),
        ("period1", get_finance_data_dates(stock)[0].split("/")[1]),
        ("year2", get_finance_data_dates(stock)[1].split("/")[0]),
        ("period2", get_finance_data_dates(stock)[1].split("/")[1]),
        ("year3", get_finance_data_dates(stock)[2].split("/")[0]),
        ("period3", get_finance_data_dates(stock)[2].split("/")[1]),
        ("year4", get_finance_data_dates(stock)[3].split("/")[0]),
        ("period4", get_finance_data_dates(stock)[3].split("/")[1]),
        ),
        (
        ("companyCode", stock),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", get_finance_data_dates(stock)[4].split("/")[0]),
        ("period1", get_finance_data_dates(stock)[4].split("/")[1]),
        ("year2", get_finance_data_dates(stock)[5].split("/")[0]),
        ("period2", get_finance_data_dates(stock)[5].split("/")[1]),
        ("year3", get_finance_data_dates(stock)[6].split("/")[0]),
        ("period3", get_finance_data_dates(stock)[6].split("/")[1]),
        ("year4", get_finance_data_dates(stock)[7].split("/")[0]),
        ("period4", get_finance_data_dates(stock)[7].split("/")[1]),
        ),
        (
        ("companyCode", stock),
        ("exchange", "TRY"),
        ("financialGroup", grup),
        ("year1", get_finance_data_dates(stock)[8].split("/")[0]),
        ("period1", get_finance_data_dates(stock)[8].split("/")[1]),
        ("year2", get_finance_data_dates(stock)[9].split("/")[0]),
        ("period2", get_finance_data_dates(stock)[9].split("/")[1]),
        ("year3", get_finance_data_dates(stock)[10].split("/")[0]),
        ("period3", get_finance_data_dates(stock)[10].split("/")[1]),
        ("year4", get_finance_data_dates(stock)[11].split("/")[0]),
        ("period4", get_finance_data_dates(stock)[11].split("/")[1]),
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

def get_ready_ratio(stock, path):
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+stock
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dom = etree.HTML(str(soup))

    return float(dom.xpath(path)[0].text.replace(",", "."))


def get_ready_ratio_tradingview(stock, path):
    url = f"https://tr.tradingview.com/symbols/{stock}/financials-statistics-and-ratios/"

    driver.get(url)
    
    time.sleep(4)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))

    return float(remove_unicode_control_characters(dom.xpath(path)[0].text))

def get_ready_historical_ratio_tradingview(stock, path):
    url = f"https://tr.tradingview.com/symbols/{stock}/financials-statistics-and-ratios/"

    driver.get(url)
    
    time.sleep(4)
    
    element = driver.find_elements("xpath",path)[0]

    # Elementin çocuklarını seçin ve metinlerini alın
    child_elements = element.find_elements("xpath", "./*")
    child_texts = [remove_unicode_control_characters(child.text) for child in child_elements]

    return child_texts.reverse()

def get_ready_ratio_tradingview_summary(stock, path):
    url = f"https://tr.tradingview.com/symbols/{stock}/"

    driver.get(url)

    time.sleep(4)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))

    return float(dom.xpath(path)[0].text)


def get_ready_ratio_tradingview_test(stock, path):
    url = f"https://tr.tradingview.com/symbols/{stock}/financials-statistics-and-ratios/"

    driver.get(url)

    time.sleep(4)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))

    return float(remove_unicode_control_characters(dom.xpath(path)[0].text))

def get_historical_hbk(stock):
    url = f"https://tr.tradingview.com/symbols/BIST-{stock}/financials-income-statement/earnings-per-share-basic/"

    driver.get(url)

    time.sleep(4)
    
    def text_returner(element):
        return element.text

    historical_hbk = driver.find_elements("xpath", "//div[@class='item-CbBHHTvu']/div[2]")
    
    historical_hbk = list(map(text_returner, historical_hbk))
    
    historical_hbk = list(map(remove_unicode_control_characters, historical_hbk))[1:4]

    return historical_hbk