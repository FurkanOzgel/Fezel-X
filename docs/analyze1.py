'''
1-) Şirket ne yapıyor? Şirket faaliyetleri neler? Basit hızlı bir araştırma. 

2-) https://www.kap.org.tr/tr/sirket-bilgileri/ozet/4028e4a2416e696c01416edd70713183
    burada bildirim sorgulamaya basarak son kaplar incelenecek ve ciddi bir durum olup olmadığı kontrol edilecek.
'''

import os

def news():
    url = "https://www.kap.org.tr/tr/"
    os.system(f"google-chrome {url}")
