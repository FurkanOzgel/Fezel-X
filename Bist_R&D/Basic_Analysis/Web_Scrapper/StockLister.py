import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

url = "https://www.kap.org.tr/tr/bist-sirketler"


html = requests.get(url).text

# with open("index.html", "w") as html:
#     html.writelines(res)

# print(res)

soup = BeautifulSoup(html, 'html.parser')

# symbols = []

symbols = soup.findAll('div', class_='_04')

df = pd.DataFrame(columns=["Stock", "Sector"])

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

            newRow = {"Stock": symbol.text[1:-1], "Sector": sector}
            print(newRow)

            df = df._append(newRow, ignore_index=True)
    except IndexError:
        continue

print(df)

df.to_csv("Bist_R&D/Basic_Analysis/StockList.csv")
