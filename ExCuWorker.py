import requests
import json


def getCurExRates():
    url = "https://api.coinlore.net/api/exchange/?id=5"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    data = requests.get(url,headers=headers).text
    decode_data = json.loads(data)
    return decode_data


def monitor(basecoin: str, quotecoin: str):
    data= getCurExRates()
    for item in data['pairs']:
        if (item['base']==basecoin and item['quote']==quotecoin):
            return item['price']


def isCurrencyValid(currency: str, baseOrQuote: bool) -> bool:
    data = getCurExRates()
    cur = 'base' if baseOrQuote else 'quote' 
    for item in data['pairs']:
        if (item[cur]==currency):
            return True
    return False