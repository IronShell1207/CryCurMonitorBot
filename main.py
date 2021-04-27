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

sleeptimer = 66

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
        valuechanging =""
        if NewCryptoTask.rofl == True: 
            valuechanging= "Raise 📈" 
        else: 
            valuechanging="Fall 📉"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}\nYou have selected: {valuechanging}", reply_markup=None)
        for item in TasksList:
            if item.base == NewCryptoTask.base and item.quote == NewCryptoTask.quote and item.rofl == NewCryptoTask.rofl :
                bot.send_message(chat_id=call.message.chat.id, text=f"You already have same task: {NewCryptoTask.base}/{NewCryptoTask.quote}.\n{item.ToString()}\n\nDisable this task and create new one!")
                return    
       
        bot.send_message(chat_id=call.message.chat.id, text=f"Your task succesuffuly created. \nDetails of your task:\n{NewCryptoTask.ToString()}\n\nTo add new send /createtask\nTo start tasks send /startalltasks")
        TasksList.append(NewCryptoTask)
    if "disable" in call.data:
        idtask = str(call.data).split('/')[-1]
        TasksList[int(idtask)-1].enable=False
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}\nDisabled!", reply_markup=None)
        #bot.send_message(chat_id=call.message.chat.id, text=f"Task #{idtask} have stopped.")


def taskLoop(message, item: CryptoTask):
    while (item.enable==True):
        getprice = monitor(basecoin=item.base, quotecoin=item.quote)
        if item.rofl==True and getprice>item.price:
            print(f"Price raises to {getprice} from {item.price}")
            bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already raise 📈 to {getprice}!",reply_markup=keyboards.get_disable_task_kb(item.id))
        elif item.rofl==False and getprice<item.price:
            print(f"Price fall to {getprice} from {item.price}")
            bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already fall 📉 to {getprice}!",reply_markup=keyboards.get_disable_task_kb(item.id))
        print(f"No changes Pair: {item.base}/{item.quote}. Current price: {getprice}")
        time.sleep(sleeptimer)


@bot.message_handler(commands=['startalltasks'])
def startALLtasks(message):
    if len(TasksList) > 0:
        for item in TasksList:
            if item.enable==False:
                item.enable=True
                threadTaskloop = threading.Thread(target=taskLoop, args=[message, item])
                threadTaskloop.start()
            else: 
                bot.send_message(chat_id=message.chat.id, text=f"Your pair {item.base}/{item.quote} is already going!")
        bot.send_message(chat_id=message.chat.id, text=f"Your {len(TasksList)} monitoring tasks are started! For check all your tasks send /alltasks")
    else: 
        bot.send_message(chat_id=message.chat.id, text="You have not added any tasks yet! To add new send /createtask")

@bot.message_handler(commands=['stopalltasks'])
def stoptasks(message):
    for item in TasksList:
        item.enable=False
    bot.message_handler(chat_id=message.chat.id, text="All tasks stopped")

@bot.message_handler(func= lambda message: 'disable' in message.text )
def disabletask(message):
    ida = str(message.text).split()[-1]
    TasksList[int(ida)-1].enable=False
    bot.message_handler(chat_id=message.chat.id, text=f"Task #{ida} have stopped.")
    
    
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