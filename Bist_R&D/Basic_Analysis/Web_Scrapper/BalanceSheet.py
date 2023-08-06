import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
from selenium import webdriver
import time
import unicodedata


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


def get_ready_ratio(stock, path):
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+stock
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dom = etree.HTML(str(soup))

    return float(dom.xpath(path)[0].text.replace(",", "."))


def get_ready_ratio_tradingview(stock, path):
    url = f"https://tr.tradingview.com/symbols/{stock}/financials-statistics-and-ratios/"

    driver.get(url)

    time.sleep(7)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))

    return float(remove_unicode_control_characters(dom.xpath(path)[0].text))


def get_ready_ratio_tradingview_summary(stock, path):
    url = f"https://tr.tradingview.com/symbols/{stock}/"

    driver.get(url)

    time.sleep(7)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))

    return float(dom.xpath(path)[0].text)


def get_ready_ratio_tradingview_test(stock, path):
    url = f"https://tr.tradingview.com/symbols/{stock}/financials-statistics-and-ratios/"

    driver.get(url)

    time.sleep(7)

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    dom = etree.HTML(str(soup))

    return float(remove_unicode_control_characters(dom.xpath(path)[0].text))
