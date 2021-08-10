import requests
import json

url = "https://droidapps.cf/Files/Updates/cryptomon.json"


def checkupdates():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    versiongetter = requests.get(url, headers=headers)
    versionjs = json.loads(versiongetter)
    
    
def get_current_ver():
    pass