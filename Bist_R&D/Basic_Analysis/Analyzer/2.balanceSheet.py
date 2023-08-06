import sys
import os

parent_path= os.path.abspath(os.path.join(os.path.dirname(__file__), '../Web_Scrapper'))

sys.path.append(parent_path)

from RatioCalculator import calculate_ratios

def analyseCariOran(symbol):
    calculate_ratios(symbol)
    
analyseCariOran("PENTA")