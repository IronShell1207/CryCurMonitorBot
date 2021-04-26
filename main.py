import os
import threading
import telebot
import json
import urllib.request
import requests
import time
import config
import sys

bot = telebot.TeleBot(token=config.TOKEN)

def monitor(basecoin: str, quotecoin: str):
    url = "https://api.coinlore.net/api/exchange/?id=5"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    data = requests.get(url,headers=headers).text
    decode_data = json.loads(data)
    for item in decode_data['pairs']:
        if (item['base']==basecoin and item['quote']==quotecoin):
            return item['price']    


@bot.message_handler(commands=['give'])
def addcurr(message):
    echo = bot.send_message(chat_id=message.chat.id ,text= "Пришли новый запрос")
    bot.register_next_step_handler(message=echo, callback=secstep, args=['some text'])
    
    #for i in range(5):
    #    thread = threading.Thread(thread=monitor,args=["RVN","USDT"])
    #    update.add_handler()

def secstep(message, smsm):   
    bot.send_message(chat_id=message.chat_id,text= smsm+"\ngetted")

def main_loop():
    bot.polling(none_stop=True)

    
if (__name__=="__main__"):
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr+ '\nExiting by user request\n')
        sys.exit(0)

#https://rest.coinapi.io/v1/exchangerate/LTC/USDT?apikey=35A30795-914A-447C-9238-9265B9DB55C4
#https://docs.coinapi.io/#endpoints-2
#https://rest.coinapi.io/v1/exchangerate/BTC?apikey=35A30795-914A-447C-9238-9265B9DB55C4