from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from webScrapper import getPriceData
import json

black_list = [
    "https://tr.investing.com/indices/ise-100",
    "https://tr.investing.com/indices/germany-30",
    "https://tr.investing.com/indices/us-30",
    "https://tr.investing.com/indices/us-spx-500-futures?cid=1175153",
    "https://tr.investing.com/indices/japan-ni225",
    "https://tr.investing.com/indices/uk-100",
    "https://tr.investing.com/currencies/us-dollar-index"

]

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

driver = webdriver.Chrome( desired_capabilities=caps )

driver.get("https://tr.investing.com/equities/turkey")

time.sleep(10)

span_elements = driver.find_elements("xpath","//span[contains(@class, 'block text-ellipsis overflow-hidden whitespace-nowrap')]")
a_elements = driver.find_elements("xpath","//a[contains(@class, 'inv-link bold datatable_cell--name__link__tmnQz')]")

href_list = []

for a in a_elements:
    href = a.get_attribute("href")
    if a.text != "" and href not in black_list:
        # print(href)
        href_list.append(href)

driver.quit()

json_object = []




for i in range(18):

    print(" ")
    
    print(i)
    print(href_list[i])
    getPriceData(href_list[i])
    



with open("bist_difference.json", "w") as file:
    file.write(json.dump(json_object, file))
