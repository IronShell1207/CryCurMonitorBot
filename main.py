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
sleeptimer = 90
USERlist=[]


tasksjsn = CT.get_json_task_list()
if tasksjsn != None:
    TasksList=tasksjsn
# Добавить обработку при завершении создания таска, удаление из списка и редактирования путем полного перезаписывания файла 


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
#0-й этап
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
# 1-й этап Переадресация с main сюда
def crtask_baseset(message):
    global NewCryptoTask
    NewCryptoTask = CT.CryptoTask(user_id=message.chat.id)
    NewCryptoTask.base = message.text.upper()
    if ExCuWorker.isCurrencyValid(NewCryptoTask.base, True):
        echo = bot.send_message(chat_id=message.chat.id, text=f"Your base currency: {NewCryptoTask.base}. Now please send the quote currency (for example: 'USDT')")
        bot.register_next_step_handler(message=echo, callback=crtask_quoteset)
    else:
        bot.send_message(chat_id=message.chat.id, text="You have sent wrong currency name!\nTask creation aborted. Send /createtask again", reply_markup = keyboards.get_startup_keys())
#2-й этап    
def crtask_quoteset(message):
    global NewCryptoTask
    NewCryptoTask.quote = message.text.upper()
    if ExCuWorker.isCurrencyValid(NewCryptoTask.quote, False):
        echo = bot.send_message(chat_id=message.chat.id, text=f"You have setted the pair: {NewCryptoTask.base}/{NewCryptoTask.quote}. Now send me the price witch you want to get (for example: '0.33')")
        bot.register_next_step_handler(message=echo,callback=crtask_priceset)
    else:
        bot.send_message(chat_id=message.chat.id, text="You have sent wrong currency name!\nTask creation aborted. Send /createtask again", reply_markup = keyboards.get_startup_keys())
#3Й-этап
def crtask_priceset(message):
    global NewCryptoTask
    try:
        NewCryptoTask.price = float(message.text)
        echo = bot.send_message(chat_id=message.chat.id, text=f"Should the price rise or fall to this price? ", reply_markup = keyboards.get_raise_fall_kb())
    except (ValueError):
       echo = bot.send_message(chat_id=message.chat.id, text=f"You have sent wrong value! Task creation aborted! Send /createtask again.", reply_markup = keyboards.get_startup_keys())
#4-й этап (создание таска)
def crtask_rofl(message, data):
    global NewCryptoTask
    global TasksList
    NewCryptoTask.rofl = True if data == "CreateRaise" else False
    valuechanging = "Raise 📈" if NewCryptoTask.rofl else "Fall 📉"
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}\nYou have selected: {valuechanging}", reply_markup=None)
    for item in TasksList:
        if NewCryptoTask.id == item.id:
            NewCryptoTask.id += 1
        if item.base == NewCryptoTask.base and item.quote == NewCryptoTask.quote and item.rofl == NewCryptoTask.rofl and item.user_id == NewCryptoTask.user_id :
            bot.send_message(chat_id=message.chat.id, text=f"You already have same task: {NewCryptoTask.base}/{NewCryptoTask.quote}.\n{item.ToString()}\n\You must edit or delete it!", reply_markup=keyboards.get_remove_edit_kb(item.id))
            return
    bot.send_message(chat_id=message.chat.id, 
    text=f"""Your task succesuffuly created. \nDetails of your task:
    {NewCryptoTask.ToString()}\n\nTo add new send /createtask\nTo start tasks send /startalltasks""", 
                    reply_markup=keyboards.get_starttask_keys(NewCryptoTask.id))
    TasksList.append(NewCryptoTask)
    CT.write_json_tasks(TasksList)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#Обработки call-backov 
@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def handshit(message):
    bot.send_message(chat_id=message.chat.id, text="I dont accept this. I will send it to my admin!!")
    
@bot.message_handler(func= lambda message: 'disable' in message.text, content_types=['text'])
def disable_task(message, idz: int = -1):
    try:
        if idz == -1:
            received_id = int(str(message.text).split()[-1])
            for item in TasksList:
                if received_id == item.id and item.user_id == message.chat.id:
                    idz = item.id
            if idz == -1:
                bot.send_message(chat_id=message.chat.id, text="You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
                return   
        TasksList[idz].enable=False
        bot.send_message(chat_id=message.chat.id, text="❗️Monitoring disabled for selected ID")
        CT.write_json_tasks(TasksList)
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="❌Missing task ID", reply_markup=keyboards.get_startup_keys())

@bot.message_handler(func= lambda message: 'edittask' in message.text, content_types=['text'] )
def edit_task(message, idz: int = -1):
    global NewCryptoTask
    try:
        if idz == -1:
            received_id = int(str(message.text).split()[-1])
            for item in TasksList:
                if received_id == item.id and item.user_id == message.chat.id:
                    idz = item.id
            if idz == -1:
                bot.send_message(chat_id=message.chat.id, text="You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
                return
        TasksList[idz].enable = False
        echo = bot.send_message(chat_id=message.chat.id, text="For edit price send the new one.\nFor example: 56000")
        NewCryptoTask = TasksList[idz]
        TasksList.remove(NewCryptoTask)
        bot.register_next_step_handler(message=echo,callback=crtask_priceset)
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="❌Missing task ID", reply_markup=keyboards.get_startup_keys())
    
    
@bot.message_handler(func= lambda message: 'remove' in message.text, content_types=['text'])
def remove_task(message, idz: int = -1):
    try:
        if idz == -1:
            received_id = int(str(message.text).split()[-1])
            for item in TasksList:
                if received_id == item.id and item.user_id == message.chat.id:
                    idz = item.id
                    
            if idz == -1:
                bot.send_message(chat_id=message.chat.id, text="You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
                return
        item = TasksList[idz]
        item.enable=False
        bot.send_message(chat_id=message.chat.id, text=f"⭕️ Pair ID {item.id} {item.base}/{item.quote} removed!")
        TasksList.remove(item)
        CT.write_json_tasks(TasksList)
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="❌Missing task ID", reply_markup=keyboards.get_startup_keys())
    

@bot.message_handler(func= lambda message: 'start' in message.text, content_types=['text'])
def start_task(message, idz: int = -1):
    try:
        if idz == -1:
            received_id = int(str(message.text).split()[-1])
            for item in TasksList:
                if received_id == item.id and item.user_id == message.chat.id:
                    idz = item.id   
            if idz == -1:
                bot.send_message(chat_id=message.chat.id, text="You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
                return
        TasksList[idz].enable = True
        bot.send_message(chat_id=message.chat.id, text=f"✅ Pair {TasksList[idz].base}/{TasksList[idz].quote} is now monitoring!")
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="❌Missing task ID", reply_markup=keyboards.get_startup_keys())

# Не требует доработки
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

# Не требует доработки
@bot.message_handler(commands=['stopalltasks'])
def stoptasks(message):
    for item in TasksList:
        if item.user_id == message.chat.id and item.enable==True:
            item.enable=False
    bot.send_message(chat_id=message.chat.id, text="⛔️ All tasks are stopped.")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        if call.data == "CreateRaise" or call.data == "CreateFall":
            crtask_rofl(call.message, call.data)
        elif call.data == "createtask":
            createnewtask(call.message)
        elif call.data == "startalltasks":
            startALLtasks(call.message)
        elif call.data == "stopalltasks":
            stoptasks(call.message)
        elif call.data == "viewtasks":
            showtasks(call.message)
        #Функции ниже предназначены для обработки взаимодействий связанных с тасками напрямую
        elif "t/" in call.data:
            received_id = int(str(call.data).split('/')[-1])
            #Сразу узнаем received_id для всех операций ниже
            RealID = -1
            for item in TasksList:
                if received_id == item.id and item.user_id == call.message.chat.id:
                    RealID = item.id
            if RealID == -1:
                bot.send_message(chat_id=call.message.chat.id, text="You have sent wrong task id!")
                return
            if "disable" in call.data:
                disable_task(call.message, RealID)
            elif "edittask" in call.data:
                edit_task(call.message, RealID)
            elif "removetask" in call.data:
                remove_task(call.message, RealID)
            elif "starttask" in call.data:
                start_task(call.message, RealID)    
    except (IndexError):
        bot.send_message(chat_id=call.message.chat.id, text="🚫 Action is outdated.")  
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
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
3. Stop all monitoring tasks - /stopalltasks
4. Show all tasks /showtasks
5. Disable monitoring by ID - /disable <id>
6. Start monitoring by ID - /start <id>
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
        Binf = str(bot.get_me()).replace("'",'"').replace('None','"None"').replace('False','"False"').replace('True','"True"')
        botinfo = json.loads(Binf)
        print(f"Bot have been started. \nID: {botinfo['id']}\nName: {botinfo['first_name']}\nUserName: {botinfo['username']} ")
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