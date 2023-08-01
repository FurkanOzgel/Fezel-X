from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from lxml import etree

def getPriceData(url):
    try:
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"

        driver = webdriver.Chrome( desired_capabilities=caps )
        driver.get(url)

        time.sleep(7)

        html = driver.page_source
        
        driver.quit()
        
        soup = BeautifulSoup(html , 'html.parser')
        
        high_xpath = "/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div[5]/div[1]/dl[1]/div[4]/dd/span[3]/span[2]"
        now_xpath = "/html/body/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]"


        # Öğeyi XPath ile seç
        dom = etree.HTML(str(soup))

        high = dom.xpath(high_xpath)[0].text
        now = dom.xpath(now_xpath)[0].text

        difference = 100 - (float(now.replace(".", "").replace(",", ".")) * 100 / float(high.replace(".", "").replace(",", ".")))

        print(f"Anlık Fiyat: {now}")
        print(f"Rekor Fiyat: {high}")

        print(f"%{str(round(difference, 2))} Aşşağıda")

    except Exception as e:
        # print(e)
        getPriceData(url)
