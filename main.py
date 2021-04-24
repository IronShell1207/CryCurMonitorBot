import os
import threading
import telegram
import json
import urllib.request
import requests
from typing import List

def main():
    url = "https://api.coinlore.net/api/exchange/?id=5"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    data = requests.get(url,headers=headers).text
    decode_data = json.loads(data)
    for item in decode_data['pairs']:
        if (item['base']=="BTC"):
            print(item['price'])
    
if (__name__=="__main__"):
    main()

#https://rest.coinapi.io/v1/exchangerate/LTC/USDT?apikey=35A30795-914A-447C-9238-9265B9DB55C4
#https://docs.coinapi.io/#endpoints-2
#https://rest.coinapi.io/v1/exchangerate/BTC?apikey=35A30795-914A-447C-9238-9265B9DB55C4