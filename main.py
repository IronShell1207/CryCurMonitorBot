import os
import threading
import telegram
import json
import urllib.request
import requests
import time

from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CallbackQueryHandler, CommandHandler, ConversationHandler
from telegram.utils.request import Request

def monitor(basecoin: str, quotecoin: str):
    url = "https://api.coinlore.net/api/exchange/?id=5"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    data = requests.get(url,headers=headers).text
    decode_data = json.loads(data)
    for item in decode_data['pairs']:
        if (item['base']==basecoin and item['quote']==quotecoin):
            return item['price']    

def main():
    bot= Bot(token = "")
    
if (__name__=="__main__"):
    main()

#https://rest.coinapi.io/v1/exchangerate/LTC/USDT?apikey=35A30795-914A-447C-9238-9265B9DB55C4
#https://docs.coinapi.io/#endpoints-2
#https://rest.coinapi.io/v1/exchangerate/BTC?apikey=35A30795-914A-447C-9238-9265B9DB55C4