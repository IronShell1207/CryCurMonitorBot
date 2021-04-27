import os
import threading
import telebot
import json
import urllib.request
import requests
import time
import config
import sys
import itertools

import keyboards

bot = telebot.TeleBot(token=config.TOKEN)


TasksList = []
class CryptoTask(object):
    def __init__(self, id : int = 1 , base : str ="", quote : str ='', price : float =0.0, rofl : bool =False, enable : bool=False):
        self.id = len(TasksList)+1
        self.base = base
        self.quote = quote
        self.price = price
        self.rofl = rofl
        self.enable = enable
    
    def ToString(self) -> str:
        arr = ">" if self.rofl else "<"
        return f"Currency monitor task #{self.id}.\n\nEnabled: {self.enable}\nBase currency: {self.base}\nQuote currency: {self.quote}\nWaiting for price: {arr}{self.price}"


NewCryptoTask = CryptoTask()


def monitor(basecoin: str, quotecoin: str):
    url = "https://api.coinlore.net/api/exchange/?id=5"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    data = requests.get(url,headers=headers).text
    decode_data = json.loads(data)
    for item in decode_data['pairs']:
        if (item['base']==basecoin and item['quote']==quotecoin):
            return item['price']    



@bot.message_handler(commands=['createtask'])
def createnewtask(message):
    global NewCryptoTask
    NewCryptoTask = CryptoTask()
    echo = bot.send_message(chat_id=message.chat.id ,text="Ok. For create new task send crypto currency name. For example: 'BTC' or 'RVN'")
    bot.register_next_step_handler(message=echo, callback=createnewtask_2step)

def createnewtask_2step(message):
    global NewCryptoTask
    NewCryptoTask.base = message.text.upper()
    echo = bot.send_message(chat_id=message.chat.id, text=f"Your base currency set as: {NewCryptoTask.base}. Now please send the quote currency (for example: 'USDT')")
    bot.register_next_step_handler(message=echo, callback=createnewtask_3step)

def createnewtask_3step(message):
    global NewCryptoTask
    NewCryptoTask.quote = message.text.upper()
    echo = bot.send_message(chat_id=message.chat.id, text=f"You have setted the pair: {NewCryptoTask.base}/{NewCryptoTask.quote}. Now send me the price witch you want to get (for example: '0.33')")
    bot.register_next_step_handler(message=echo,callback=createnewtask_4step)

def createnewtask_4step(message):
    global NewCryptoTask
    NewCryptoTask.price = float(message.text)
    echo = bot.send_message(chat_id=message.chat.id, text=f"Should the price rise to this value or fall? ",reply_markup=keyboards.get_raise_fall_kb())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global NewCryptoTask
    global TasksList
    if call.data == "CreateRaise" or call.data == "CreateFall":
        if call.data == "CreateRaise":
            NewCryptoTask.rofl = True
        elif call.data == "CreateFall":
            NewCryptoTask.rofl = False
        bot.send_message(chat_id=call.message.chat.id, text=f"Your task succesuffuly created. \nDetails of your task:\n{NewCryptoTask.ToString()}")
        TasksList.append(NewCryptoTask)
        

taskloopenabled = false
threadTaskloop

def taskLoop(message):
    for item in TasksList:
        while (item.enable==True):
            getprice = monitor(basecoin=item.base, quotecoin=item.quote)
            if item.rofl==true and getprice>item.price:
                bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already raise 📈 to {getprice}!")
            elif item.rofl==false and getprice<item.price:
                bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already fall 📉 to {getprice}!")
            time.sleep(30000)


@bot.message_handler(commands=['starttasks'])
def starttasks(message):
    global threadTaskloop
    if taskloopenabled==True:
        bot.send_message(chat_id=message.chat.id, "Tasks already started! To stop send /stoptaasks")
        return
    elif taskloopenabled==False and TasksList.len > 0:
        threadTaskloop = threading.Thread(target=taskLoop, args=[message])
        threadTaskloop.start()
        bot.send_message(chat_id=message.chat.id, text=f"Your {TasksList.len} monitoring tasks are started! For check all your tasks send /alltasks")
    else: bot.send_message(chat_id=message.chat.id, text="You have not added any tasks yet! To add new send /createtask")

@bot.message_handler(commands=['start'])
def start(message):
    echo = bot.send_message(chat_id=message.chat.id, text="Hello! I'm crypto currency exchange monitor bot. I can send you notification when your currency is raise or fall to setted value. For create new task send: /createtask.")

def secstep(message, smsm):   
    bot.send_message(chat_id=message.chat.id,text= smsm+"\ngetted")

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