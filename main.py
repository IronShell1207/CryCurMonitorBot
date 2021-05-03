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
import datetime
import re

import ExCuWorker
import CryptoTask as CT
import keyboards

TasksList = []
tof = config.TOKEN if input('Choose your destiny: 1 - release, 2 - dev\n')=='1' else config.TOKEN_px
bot = telebot.TeleBot(token=tof)

mainthread = threading.Thread()
sleeptimer = 70
USERlist=[]


tasksjsn = CT.get_json_task_list()
if tasksjsn != None:
    TasksList=tasksjsn
# Добавить обработку при завершении создания таска, удаление из списка и редактирования путем полного перезаписывания файла 

# Переадресация с main сюда
def crtask_baseset(message):
    global NewCryptoTask
    NewCryptoTask = CT.CryptoTask(user_id=message.chat.id)
    NewCryptoTask.base = message.text.upper()
    if ExCuWorker.isCurrencyValid(NewCryptoTask.base, True):
        echo = bot.send_message(chat_id=message.chat.id, text=f"Your base currency: {NewCryptoTask.base}. Now please send the quote currency (for example: 'USDT')")
        bot.register_next_step_handler(message=echo, callback=crtask_quoteset)
    else:
        bot.send_message(chat_id=message.chat.id, text="You have sent wrong currency name!\nTask creation aborted. Send /createtask again")
        

def crtask_quoteset(message):
    global NewCryptoTask
    NewCryptoTask.quote = message.text.upper()
    if ExCuWorker.isCurrencyValid(NewCryptoTask.quote, False):
        echo = bot.send_message(chat_id=message.chat.id, text=f"You have setted the pair: {NewCryptoTask.base}/{NewCryptoTask.quote}. Now send me the price witch you want to get (for example: '0.33')")
        bot.register_next_step_handler(message=echo,callback=crtask_priceset)
    else:
        bot.send_message(chat_id=message.chat.id, text="You have sent wrong currency name!\nTask creation aborted. Send /createtask again")


def crtask_priceset(message):
    global NewCryptoTask
    #       try:
    NewCryptoTask.price = float(message.text)
    echo = bot.send_message(chat_id=message.chat.id, text=f"Should the price rise to this value or fall? ",reply_markup=keyboards.get_raise_fall_kb())
    #except:
    #   echo = bot.send_message(chat_id=message.chat.id, text=f"Price is incorrect! Task creation aborted! Send /createtask again.")


def crtask_rofl(message,data):
    global NewCryptoTask
    global TasksList
    NewCryptoTask.rofl = True if data == "CreateRaise" else False
    valuechanging = "Raise 📈" if NewCryptoTask.rofl else "Fall 📉"
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}\nYou have selected: {valuechanging}", reply_markup=None)
    for item in TasksList:
        if NewCryptoTask.id == item.id:
            NewCryptoTask.id+=1
        if item.base == NewCryptoTask.base and item.quote == NewCryptoTask.quote and item.rofl == NewCryptoTask.rofl and item.user_id == NewCryptoTask.user_id :
            bot.send_message(chat_id=message.chat.id, text=f"You already have same task: {NewCryptoTask.base}/{NewCryptoTask.quote}.\n{item.ToString()}\n\nDisable this task and create new one!", reply_markup=keyboards.get_remove_edit_kb(item.id))
            return    
    bot.send_message(chat_id=message.chat.id, 
    text=f"""Your task succesuffuly created. 
Details of your task:
{NewCryptoTask.ToString()}\n\nTo add new send /createtask
To start tasks send /startalltasks""", 
                    reply_markup=keyboards.get_starttask_keys(NewCryptoTask.id))
    TasksList.append(NewCryptoTask)
    CT.write_json_tasks(TasksList)
    

def disable_task(message, idz):
    TasksList[int(idz)].enable=False
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}\n❗️Disabled", reply_markup=None)
    CT.write_json_tasks(TasksList)


def edit_task(message,idz):
    global NewCryptoTask
    if (message.chat.id == TasksList[int(idz)].user_id):
        TasksList[int(idz)].enable=False
        echo = bot.send_message(chat_id=message.chat.id, text="For edit price send the new one.\nFor example: 0.0004010")
        NewCryptoTask = TasksList[int(idz)]
        TasksList.remove(NewCryptoTask)
        bot.register_next_step_handler(message=echo,callback=crtask_priceset)
    else: raise Exception("No such task id from this user")
    

def remove_task(message, idx):
    item = TasksList[idx]
    if message.chat.id == item.user_id:
        item.enable=False
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}", reply_markup=None)
        bot.send_message(chat_id=message.chat.id, text=f"⭕️ Pair ID {item.id} {item.base}/{item.quote} removed!")
        TasksList.remove(item)
        CT.write_json_tasks(TasksList)
    else: raise Exception("No such task id from this user")

def start_task(message, idx: int):
    item = TasksList[idx]
    if message.chat.id == item.user_id:
        item.enable=True
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}", reply_markup=None)
        bot.send_message(chat_id=message.chat.id, text=f"✅ Pair {item.base}/{item.quote} is now monitoring!")
    else: raise Exception("No such task id from this user")




@bot.message_handler(commands=['createtask'])
def createnewtask(message):
    global mainthread
    global USERlist
    echo = bot.send_message(chat_id=message.chat.id ,text="For create new crypto currency monitoring task send crypto currency name, for example: 'BTC' or 'RVN'")
    bot.register_next_step_handler(message=echo, callback=crtask_baseset)
    if message.chat.id not in USERlist:
        mainthread = threading.Thread(target=tasks_loop,args=[message])
        mainthread.start()
        USERlist.append(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "CreateRaise" or call.data == "CreateFall":
            crtask_rofl(call.message, call.data)
        elif "t/" in call.data:
            idtask = int(str(call.data).split('/')[-1])
            if "disable" in call.data:
                disable_task(call.message,idtask)
            elif "edittask" in call.data:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}", reply_markup=None)
                edit_task(call.message, idtask)
            elif "removetask" in call.data:
                remove_task(call.message, idtask)
            elif "starttask" in call.data:
                start_task(call.message,idtask)
        elif call.data == "createtask":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
            createnewtask(call.message)
        elif call.data == "startalltasks":
            startALLtasks(call.message)
        elif call.data == "stopalltasks":
            stoptasks(call.message)
    except (IndexError):
        bot.send_message(chat_id=call.message.chat.id, text="🚫 Action is outdated.")  


@bot.message_handler(commands=['startalltasks'])
def startALLtasks(message):
    if len(TasksList) > 0:
        if message.chat.id not in USERlist:
            mainthread = threading.Thread(target=tasks_loop,args=[message])
            mainthread.start()
            USERlist.append(message.chat.id)
        i = 0
        for item in TasksList:
            if message.chat.id == item.user_id:
                if item.enable==False:
                    item.enable=True
                    i+=1
                else: 
                    bot.send_message(chat_id=message.chat.id, text=f"Your pair {item.base}/{item.quote} is already going!")
        bot.send_message(chat_id=message.chat.id, text=f"Your {i} monitoring tasks are started! For check all your tasks send /showtasks")
    else: 
        bot.send_message(chat_id=message.chat.id, text="You have not added any tasks yet! To add new send /createtask")


@bot.message_handler(commands=['stopalltasks'])
def stoptasks(message):
    for item in TasksList:
        if item.user_id == message.chat.id and item.enable==True:
            item.enable=False
    bot.send_message(chat_id=message.chat.id, text="All tasks stopped")



@bot.message_handler(func= lambda message: 'disable' in message.text )
def disabletask(message):
    ida = int(str(message.text).split()[-1])
    try:
        TasksList[int(ida)-1].enable=False
        bot.send_message(chat_id=message.chat.id, text=f"Task #{ida} have stopped.")
    except:
        bot.send_message(chat_id=message.chat.id, text=f"Missing task ID")


@bot.message_handler(func= lambda message: 'edittask' in message.text )
def disabletask(message):
    ida = int(str(message.text).split()[-1])
    try:
        edit_task(message,ida)
    except:
        bot.send_message(chat_id=message.chat.id, text=f"Missing task ID")

@bot.message_handler(func= lambda message: 'enable' in message.text )
def edittask(message):
    ida = str(message.text).split()[-1]
    try:
        TasksList[int(ida)-1].enable=True
        bot.send_message(chat_id=message.chat.id, text=f"Task #{ida} have started.")
    except:
        bot.send_message(chat_id=message.chat.id, text=f"Missing task ID")
    
    
@bot.message_handler(commands=['showtasks'])
def showtasks(message):
    if message.chat.id not in USERlist:
        mainthread = threading.Thread(target=tasks_loop,args=[message])
        mainthread.start()
        USERlist.append(message.chat.id)
    printer = ""
    for item in TasksList:
        if item.user_id == message.chat.id:
            printer += item.ToShortStr()+"\n"
    bot.send_message(chat_id=message.chat.id, text=f"Your monitoring task list:\n{printer}", reply_markup=keyboards.get_en_dis_all_keys())

    
@bot.message_handler(commands=['start'])
def start(message):
    echo = bot.send_message(chat_id=message.chat.id, 
    text="Hello! I'm crypto currency exchange monitor bot. I can send you notification when your currency is raise or fall to setted value. \nFor create new task send: /createtask.",
    reply_markup=keyboards.get_startup_keys())


@bot.message_handler(commands=['help'])
def help(message):
    echo = bot.send_message(chat_id=message.chat.id,
                            text="""Commands list:
1. Create new monitoring task - /createtask
2. Start all monitoring tasks - /startalltasks
3.Stop all monitoring tasks - /stopalltasks
4. Show all tasks /showtasks
5. Disable monitoring by ID - /disable <id>
6. Enable monitoring by ID - /enable <id>
7. Edit task - /edit <id>""")
    

def tasks_loop(message):
    while(True):
        for item in TasksList:
            if message.chat.id == item.user_id and item.enable==True:
                getprice = ExCuWorker.monitor(basecoin=item.base, quotecoin=item.quote)
                ipr = item.price if item.price>1 else "{:^10.8f}".format(item.price)
                gpr = getprice if getprice>1 else "{:^10.8f}".format(getprice)
                if item.rofl==True and getprice>item.price:
                    print(f'[{datetime.datetime.now().time()}] {item.base}/{item.quote}. Price raises to {gpr} from {ipr}')
                    bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already raise 📈 to {gpr}!",reply_markup=keyboards.get_disable_task_kb(item.id))
                elif item.rofl==False and getprice<item.price:
                    print(f'[{datetime.datetime.now().time()}] {item.base}/{item.quote}. Price fall to {gpr} from {ipr}')
                    bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already fall 📉 to {gpr}!",reply_markup=keyboards.get_disable_task_kb(item.id))
                else: 
                    print(f"[{datetime.datetime.now().time()}] {item.base}/{item.quote}. Current price: {gpr}; Task id: {item.id}, User id: {item.user_id}")
            time.sleep(1)
        time.sleep(sleeptimer)    
        #print("Alive")
                    
            

def main_loop():
    try:
        print(bot.get_me())
        bot.polling(none_stop=True) 

    except ConnectionError:
        time.sleep(5)
        main_loop()

    
if (__name__=="__main__"):
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr+ '\nExiting by user request\n')
        sys.exit(0)

#https://rest.coinapi.io/v1/exchangerate/LTC/USDT?apikey=35A30795-914A-447C-9238-9265B9DB55C4
#https://docs.coinapi.io/#endpoints-2
#https://rest.coinapi.io/v1/exchangerate/BTC?apikey=35A30795-914A-447C-9238-9265B9DB55C4