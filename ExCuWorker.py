import requests
import json
import time
import threading
from datetime import datetime
from datetime import timedelta

TimeLastUpdate = datetime(2020, 1, 1)   
CurExRates = []


def getCurExRates():
    global TimeLastUpdate
    global CurExRates

    date = datetime.now() - timedelta(seconds=120)
    if TimeLastUpdate < date:
        CurExRates= []
        urls = ["https://api.coinlore.net/api/exchange/?id=5","https://api.coinlore.net/api/exchange/?id=17","https://api.coinlore.net/api/exchange/?id=49","https://api.coinlore.net/api/exchange/?id=66"]
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
        for url in urls:
            data = requests.get(url,headers=headers).text
            decode_data = json.loads(data)
            TimeLastUpdate = date + timedelta(seconds=160)
            for item in decode_data['pairs']:
                CurExRates.append(item)
        print(f'[{datetime.now().time()}] Crypto data have been updated.')
    return CurExRates


def monitor(basecoin: str, quotecoin: str) -> float:
    for i in range(4):
        data = getCurExRates()
        for item in data:
            if (item['base']==basecoin and item['quote']==quotecoin):
                price = float(item['price'])
                price = price if price>0.0001 else "{:^10.8f}".format(price)
                return price


def isCurrencyValid(currency: str, baseOrQuote: bool) -> bool:
    for i in range(4):
        data = getCurExRates()
        cur = 'base' if baseOrQuote else 'quote' 
        for item in data:
            if (item[cur]==currency):
                return True
    return False






"""
class data_ex(object):
        def __init__(self,base: str = "",quote: str="",idbase:int = 0):
            self.base = base
            self.quote = quote
            self.idbase = idbase
class ExchangeCurBase:
    urls = ["https://api.coinlore.net/api/exchange/?id=5",
    "https://api.coinlore.net/api/exchange/?id=17",
    "https://api.coinlore.net/api/exchange/?id=49",
    "https://api.coinlore.net/api/exchange/?id=66"]
   
    data = []

    def __init__(self):
        thread = threading.Thread(target=self.update_data, args=[self])
        thread.start()
        pass

    def update_data(self):
        while(True):
            for iurl in urls:
                i = 0
                dada = getCurExRates(iurl)
                for item in dada['pairs']:
                    dat = data_ex(base=item['base'], quote=item['quote'],idbase=i)
                    self.data.append(dat)
                i+=1
            time.sleep(1000)
"""