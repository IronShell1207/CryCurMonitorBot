import requests
import json
import time
import threading
from datetime import datetime
from datetime import timedelta

from requests.api import head

TimeLastUpdate = datetime(2020, 1, 1)   
CurExRates = []

#https://www.binance.com/api/v3/ticker/price?symbol=ETHUSDT


def bin_getCur(base: str, quote: str) -> float:
    try:
        link_cur = f"https://binance.com/api/v3/ticker/price?symbol={base}{quote}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
        datareq = requests.get(link_cur,headers=headers).text
        decode_cur = json.loads(datareq)
        if decode_cur['price'] != None:
            return float(decode_cur['price'])
        else:
            return None
    except:
        return None
    
def bin_get_monitor():
    url = "https://www.binance.com/api/v3/ticker/price"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    datacur = requests.get(url,headers=headers).text
    decode_cur = json.loads(datacur)
    return decode_cur

def bin_monitor(base, quote, basecurses) -> float:
    for item in basecurses:
        if (item['symbol']==base+quote):
            price = float(item['price'])
            return price

def bin_get_pair_quotes(base):
    url = "https://www.binance.com/api/v1/exchangeInfo"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    data = requests.get(url, headers=headers).text
    quotes_stack = []
    decode_pairs = json.loads(data)
    for item in decode_pairs['symbols']:
        if item['baseAsset'] == base and item['status'] == "TRADING":
            quotes_stack.append(item['quoteAsset'])
    return quotes_stack
