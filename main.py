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

commandsRE = re.compile("/(\S+)\s(\d+)")


mainthread = threading.Thread()
sleeptimer = 90
USERlist=[]


tasksjsn = CT.get_json_task_list()
if tasksjsn != None:
    TasksList=tasksjsn
# Добавить обработку при завершении создания таска, удаление из списка и редактирования путем полного перезаписывания файла 

def checkifnewuser(message):
    for user in USERlist:
        if user.user_id == message.chat.id:
            return
    mainthread = threading.Thread(target=tasks_loop,args=[message])
    mainthread.start()
    user = CT.UserSets(user_id=message.chat.id, notifytimer = 90)
    USERlist.append(user)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
#0-й этап
@bot.message_handler(commands=['createtask'])
def createnewtask(message):
    global mainthread
    global USERlist
    echo = bot.send_message(chat_id=message.chat.id ,text="For create new crypto currency monitoring task send crypto currency name, for example: 'BTC' or 'RVN'")
    bot.register_next_step_handler(message=echo, callback=crtask_baseset)
    checkifnewuser(message)
    #if message.chat.id not in USERlist:
    #    mainthread = threading.Thread(target=tasks_loop,args=[message])
    #    mainthread.start()
    #    USERlist.append(message.chat.id)
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
    {NewCryptoTask.ToString()}\n\nTo add new send /createtask\nTo start tasks send /turnontasks""", 
                    reply_markup=keyboards.get_starttask_keys(NewCryptoTask.id))
    TasksList.append(NewCryptoTask)
    CT.write_json_tasks(TasksList)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#Обработки call-backov 
@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def handshit(message):
    bot.send_message(chat_id=message.chat.id, text="I dont accept this. I will send it to my admin!!")
    
def id_task_finder(in_id: int, user_id: int):
    i = 0
    for item in TasksList:
        if item.id == in_id and item.user_id == user_id:
            return i
        i+=1
    return -1

@bot.message_handler(func= lambda message: commandsRE.match(message.text) != None)
def task_manage_handler(message):
    try:
        match3 = commandsRE.match(message.text)
        global NewCryptoTask
        global TasksList
        taskz = match3.group(1)
        idz = int(match3.group(2))
        if (taskz == "settimer" or taskz == "timer"):
            for useri in USERlist:
                if message.chat.id == useri.user_id:
                    useri.setnewtimer(idz)
                    bot.send_message(chat_id=message.chat.id, text=f"📣Notification delay setted on {idz}sec.🕒")
                    return
        idz = id_task_finder(int(match3.group(2)), message.chat.id)
        if idz == -1:
            bot.send_message(chat_id=message.chat.id, text="🚫You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
            return   
        if (taskz == "start" or taskz == "enable"):
            TasksList[idz].enable = True
            bot.send_message(chat_id=message.chat.id, text=f"✅ Pair #{TasksList[idz].id} {TasksList[idz].base}/{TasksList[idz].quote} is now monitoring!")
        elif (taskz == "disable" or taskz == "stop"):
            TasksList[idz].enable = False
            bot.send_message(chat_id=message.chat.id, text=f"❗️Monitoring disabled for #{TasksList[idz].id} {TasksList[idz].base}/{TasksList[idz].quote}")
        elif (taskz == "edittask" or taskz == "edit"):
            TasksList[idz].enable = False
            echo = bot.send_message(chat_id=message.chat.id, text=f"You are editting pair: {TasksList[idz].base}/{TasksList[idz].quote}.\nFor edit price send the new one.\nFor example: 56000")
            NewCryptoTask = TasksList[idz]
            TasksList.remove(NewCryptoTask)
            bot.register_next_step_handler(message=echo,callback=crtask_priceset)
        elif (taskz == "remove" or taskz == "delete"):
            item = TasksList[idz]
            item.enable = False
            bot.send_message(chat_id=message.chat.id, text=f"⭕️ Pair ID {item.id} {item.base}/{item.quote} removed!")
            TasksList.remove(item)
            CT.write_json_tasks(TasksList)
        
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="❌Missing task ID", reply_markup=keyboards.get_startup_keys())

@bot.message_handler(commands=["/checkprice"])
def pricecheck(message):
    echo = bot.send_message(chat_id=message.chat.id, text="To check current exchange rates send me currency pair.\n\nFor example: BTC/USDT or RVN/BTC.\nPlease observe this pattern")
    bot.register_next_step_handler(message=echo, callback=pricechecker)

def pricechecker(message):
    pairpattern = re.compile(r'(\S+)/(\S+)').match(message.text)
    if pairpattern != None:
        basecur = pairpattern.group(1).upper()
        quotecur = pairpattern.group(2).upper()
        if ExCuWorker.isCurrencyValid(basecur, True) and ExCuWorker.isCurrencyValid(quotecur, False):
            pricecur = ExCuWorker.monitor(basecoin=basecur, quotecoin=quotecur)
            pricecur = pricecur if pricecur>0.001 else "{:^10.8f}".format(pricecur)
            bot.send_message(chat_id=message.chat.id ,text=f"💸Current price for pair {basecur}/{quotecur}: {pricecur}")
        else:
            bot.send_message(chat_id=message.chat.id ,text=f"I can't find pair {basecur}/{quotecur} in the list")
    else:
        bot.send_message(chat_id=message.chat.id, text="You send wrong call.\n You must observe pattern!")
    
# Не требует доработки
@bot.message_handler(commands=['turnontasks'])
def startALLtasks(message):
    if len(TasksList) > 0:
        checkifnewuser(message)
        #if message.chat.id not in USERlist:
        #    mainthread = threading.Thread(target=tasks_loop,args=[message])
        #    mainthread.start()
        #    USERlist.append(message.chat.id)
        i = 0
        ix = 0
        for item in TasksList:
            if message.chat.id == item.user_id:
                if item.enable==False:
                    item.enable=True
                    i+=1
                else: 
                    ix += 1
                    #bot.send_message(chat_id=message.chat.id, text=f"Your pair {item.base}/{item.quote} is already going!")
        alreadyon = f"and {ix} tasks already ON ✅" if ix>0 else ""
        bot.send_message(chat_id=message.chat.id, text=f"Your {i} monitoring tasks are started {alreadyon}\nFor check all your tasks send /showtasks")
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
        global NewCryptoTask
        global TasksList
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        if call.data == "CreateRaise" or call.data == "CreateFall":
            crtask_rofl(call.message, call.data)
        elif call.data == "createtask":
            createnewtask(call.message)
        elif call.data == "turnontasks":
            startALLtasks(call.message)
        elif call.data == "stopalltasks":
            stoptasks(call.message)
        elif call.data == "viewtasks":
            showtasks(call.message)
        #Функции ниже предназначены для обработки взаимодействий связанных с тасками напрямую
        elif "t/" in call.data:
            received_id = int(str(call.data).split('/')[-1])
            #Сразу узнаем received_id для всех операций ниже
            RealID = id_task_finder(received_id, call.message.chat.id)
            if RealID == -1:
                bot.send_message(chat_id=call.message.chat.id, text="You have sent wrong task id!")
                return
            if "disable" in call.data:
                TasksList[RealID].enable=False
                bot.send_message(chat_id=call.message.chat.id, text="❗️Monitoring disabled for selected ID")
                CT.write_json_tasks(TasksList)
            elif "edittask" in call.data:
                TasksList[RealID].enable = False
                echo = bot.send_message(chat_id=call.message.chat.id, text=f"You are editting pair: {TasksList[RealID].base}/{TasksList[RealID].quote}.\nFor edit price send the new one.\nFor example: 56000")
                NewCryptoTask = TasksList[RealID]
                TasksList.remove(NewCryptoTask)
                bot.register_next_step_handler(message=echo, callback=crtask_priceset)
            elif "removetask" in call.data:
                item = TasksList[RealID]
                item.enable = False
                bot.send_message(chat_id=call.message.chat.id, text=f"⭕️ Pair ID {item.id} {item.base}/{item.quote} removed!")
                TasksList.remove(item)
                CT.write_json_tasks(TasksList)
            elif "starttask" in call.data:
                TasksList[RealID].enable = True
                bot.send_message(chat_id=call.message.chat.id, text=f"✅ Pair {TasksList[RealID].base}/{TasksList[RealID].quote} is now monitoring!") 
    except (IndexError):
        bot.send_message(chat_id=call.message.chat.id, text="🚫 Action is outdated.")  
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
@bot.message_handler(commands=['showtasks'])
def showtasks(message):
    checkifnewuser(message)
    #if message.chat.id not in USERlist:
    #    mainthread = threading.Thread(target=tasks_loop,args=[message])
    #    mainthread.start()
    #    USERlist.append(message.chat.id)
    printer = ""
    for item in TasksList:
        if item.user_id == message.chat.id:
            printer += item.ToShortStr()+"\n"
    bot.send_message(chat_id=message.chat.id, text=f"Your monitoring task list:\n\n{printer}", reply_markup=keyboards.get_en_dis_all_keys())

    
@bot.message_handler(commands=['start'])
def start(message):
    echo = bot.send_message(chat_id=message.chat.id, 
    text="Hello! I'm crypto currency exchange monitor bot. I can send you notification when your currency is raise or fall to setted value. \nFor create new task send: /createtask.\nFor get info send: /info\nFor get all available commands send: /help",
    reply_markup=keyboards.get_main_keyboard())

@bot.message_handler(commands=['info'])
def infohelp(message):
    bot.send_message(chat_id=message.chat.id, 
                     text=f"This bot is written on Python with pyTelegramBotApi library. This bot uses data from free API: coinlore.com. Data updates every 3-5 minutes, and if you get twice same notifications it's only because of old data on API server\n⛏ Developer: Ironshell\n🛸 Github: https://github.com/IronShell1207/CryCurMonitorBot\n\nIf bot is usefull for you, you can buy my a ☕️ and thx 2u).\n🥇ETH: 0xa35fbab442da4e65413045a4b9b147e2a0fc3e0c\n🎈LTC: LQiBdMeCNWAcSBEhc2QT3ffFz8a2t7zPcG")

@bot.message_handler(commands=['setstyle'])
def setstyle(message):
    for user in USERlist:
        if message.chat.id == user.user_id:
            user.notifystyle = not user.notifystyle
            prints = "📢 Notifications about exchange rates changes now shows separately" if user.notifystyle == False else "📢 Notifications about exchange rates changes now shows jointly in single message"
            bot.send_message(chat_id=message.chat.id, text = prints)
            return

@bot.message_handler(func=lambda message: message.text in ["View my tasks 📝","Create new task 📊","Start all tasks ▶️","Disable all tasks ⏸", "Check price 💸"])
def msg_kb_handler(message):
    if message.text == "View my tasks 📝":
        showtasks(message)
    elif message.text == "Create new task 📊":
        createnewtask(message)
    elif message.text == "Start all tasks ▶️":
        startALLtasks(message)
    elif message.text == "Disable all tasks ⏸":
        stoptasks(message)
    elif message.text == "Check price 💸":
        pricecheck(message)


@bot.message_handler(commands=['help'])
def help(message):
    echo = bot.send_message(chat_id=message.chat.id,
                            text="""Commands list:
1. Create new monitoring task - /createtask
2. Start all monitoring tasks - /turnontasks
3. Stop all monitoring tasks - /stopalltasks
4. Show all tasks /showtasks
5. Disable monitoring by ID - /disable <id>
6. Start monitoring by ID - /enable <id>
7. Edit task - /edit <id>
8. Delete task /remove <id>
9. Set notification delay (secounds) - /settimer <secs>""")
    


def tasks_loop(message):
    while(True):
        style = False
        for users in USERlist:
            if users.user_id == message.chat.id:
                time.sleep(users.notifytimer) 
                style = users.notifystyle
        printer = ""
        for item in TasksList:
            if message.chat.id == item.user_id and item.enable==True:
                getprice = ExCuWorker.monitor(basecoin=item.base, quotecoin=item.quote)
                if getprice == None:
                    bot.send_message(chat_id= message.chat.id, text=f"Sorry, pair {item.base}/{item.quote} now unavailable! Task disabled!⛔️")
                    item.enable=False
                    return
                ipr = item.price if item.price>0.0001 else "{:^10.8f}".format(item.price)
                gpr = getprice if getprice>0.0001 else "{:^10.8f}".format(getprice)
                if item.rofl==True and getprice>item.price:
                    print(f'[{datetime.datetime.now().time()}] {item.base}/{item.quote}. Price raises to {gpr} from {ipr}')
                    printer += f"[ID {item.id}] {item.base}/{item.quote} already raise 📈 to {gpr}!\n"
                    if style == False:
                        bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already raise 📈 to {gpr}!",reply_markup=keyboards.get_disable_task_kb(item.id))
                        time.sleep(1)
                elif item.rofl==False and getprice<item.price:
                    print(f'[{datetime.datetime.now().time()}] {item.base}/{item.quote}. Price fall to {gpr} from {ipr}')
                    printer += f"[ID {item.id}] {item.base}/{item.quote} already fall 📉 to {gpr}!\n"
                    if style == False:
                        bot.send_message(chat_id=message.chat.id, text = f"Your pair {item.base}/{item.quote} already fall 📉 to {gpr}!",reply_markup=keyboards.get_disable_task_kb(item.id))
                        time.sleep(1)
                else: 
                    pass
                    print(f"[{datetime.datetime.now().time()}] {item.base}/{item.quote}. Current price: {gpr}; Task id: {item.id}, User id: {item.user_id}") 
        if printer != "" and style == True:
            bot.send_message(chat_id=message.chat.id, text=f"💹Your updated exchange rates list:💹\n{printer}")        
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