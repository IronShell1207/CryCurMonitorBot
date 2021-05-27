import os
import threading
from typing import Counter, Text
from requests.api import get
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
import subprocess

import ExCuWorker
import CryptoTask as CT
import keyboards
import recombos


TasksList = []
#Требуется создать файл config.py и добавить в него строку TOKEN="<ваш токен>"
tof = config.TOKEN if input('Choose your destiny: 1 - release, 2 - dev\n')=='1' else config.TOKEN_px
bot = telebot.TeleBot(token=tof)

commandsRE = re.compile("/(\S+)\s(\d+)")
createRE = re.compile("/(\S+)\s(\S{1,5})\s(\S{1,4})\s(\d+)\s(Fall|Raise)") #/createtask BTC USDT 56000 Raise


mainthread = threading.Thread()
USERlist=[]


tasksjsn = CT.get_json_task_list()
if tasksjsn != None:
    TasksList=tasksjsn

def checkifnewuser(message):
    for user in USERlist:
        if user.user_id == message.chat.id:
            return
    mainthread = threading.Thread(target=new_task_loop,args=[message])
    mainthread.start()
    user = CT.UserSets(user_id=message.chat.id, notifytimer = 30)
    USERlist.append(user)


def getUSByID(id) -> CT.UserSets:
    for user in USERlist:
        if user.user_id == id:
            return user
    bot.send_message(chat_id=id, text="It's looks like you haven't any tasks enabled!")
    return None

@bot.message_handler(func= lambda message: ('createtask' in message.text or 'create' in message.text or 'newtask' in message.text) or recombos.create_univers.match(message.text) != None)
def create_task_h(message):
    global NewCT
    try:
        NewCT = CT.CryptoTask(user_id=message.chat.id)
        cmb = recombos.create_univers.match(message.text)
        if cmb != None:
            NewCT.base = cmb.group(2).upper()
            NewCT.quote = cmb.group(4).upper()
            if cmb.group(6) == None:
                echo = bot.send_message(chat_id=message.chat.id, text=f"Pair {NewCT.base}/{NewCT.quote} created.\nSpecify the value you want to get for this pair.")
                bot.register_next_step_handler(echo, crtask_priceset)
                return
            NewCT.price = float(cmb.group(6)) if float(cmb.group(6))>0.001 else "{:^10.8f}".format(float(cmb.group(6)))
            if cmb.group(8) == None:
                bot.send_message(chat_id=message.chat.id, text = f"Pair {NewCT.base}/{NewCT.quote} with value {NewCT.price} created.\nSelect the movement of value of your pair falling or raising", reply_markup=keyboards.get_raise_fall_kb())
                return
            NewCT.rofl = True if cmb.group(8) == "+" or cmb.group(8) == "Raise" else None
            TasksList.append(NewCT)
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=message.chat.id, text = f"Your monitoring task created.\n{NewCT.ToString()}")
            return
        else:
            echo = bot.send_message(chat_id=message.chat.id, text="To create new monitoring task send me the pair witch you want to monitor.\nFirst send me base currency.\n\nExample: 'BTC' 'LTC' 'ETH' (without quotes)")
            bot.register_next_step_handler(echo, crtask_baseset)
            return
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="Error")


def crtask_baseset(message):
    global NewCT
    revalue = recombos.re_value_name.match(message.text)
    if revalue != None:
        NewCT.base = message.text.upper()
        quotes_stack = ExCuWorker.bin_get_pair_quotes(NewCT.base)
        echo = bot.send_message(chat_id=message.chat.id, text=f"Task creation\n\nYour base currency: {NewCT.base}. \nNow select quote for create pair.", reply_markup=keyboards.get_quotes_keyboard(quotes_stack))
        #bot.register_next_step_handler(message=echo, callback=crtask_quotetask)
    else:
        bot.send_message(chat_id=message.chat.id, text="🚫 Error. You have sent wrong value")


#2-й этап    
def crtask_quotetask(message):
    global NewCT
    revalue = recombos.re_value_name.match(message.text)
    if revalue != None:
        NewCT.quote = message.text.upper()
        priceex = ExCuWorker.bin_getCur(base= NewCT.base, quote= NewCT.quote)
        if (priceex != None):
            priceex = priceex if priceex>0.001 else "{:^10.8f}".format(priceex)
            echo = bot.send_message(chat_id= message.chat.id, text=f"Task creation.\nYour pair is {NewCT.base}\{NewCT.quote}.\nNow send the price, which you want to get. If exchange rates of this pair gets to this price you will get the notifications.\nExample: {priceex}")
            bot.register_next_step_handler(message=echo, callback=crtask_priceset)
        else:
            bot.send_message(chat_id=message.chat.id, text=f"🚫 Your pair is wrong. Task creation aborted")
    else:
        bot.send_message(chat_id=message.chat.id, text="🚫 Error. You have sent wrong value")


#3Й-этап
def crtask_priceset(message):
    global NewCT
    try:
        NewCT.price = float(message.text)
        NewCT.price = NewCT.price if NewCT.price>0.001 else "{:^10.8f}".format(NewCT.price)
        echo = bot.send_message(chat_id=message.chat.id, text=f"Pair: {NewCT.base}\{NewCT.quote}\nPrice: {NewCT.price}.\nShould the price rise or fall to this price?", reply_markup = keyboards.get_raise_fall_kb())
    except (ValueError):
        echo = bot.send_message(chat_id=message.chat.id, text=f"You have sent wrong value! Task creation aborted! Send /createtask again.", reply_markup = keyboards.get_startup_keys())

#4-й этап (создание таска)
def crtask_rofl(message, data):
    global NewCT
    global TasksList
    NewCT.rofl = True if data == "CreateRaise" else False
    user = getUSByID(message.chat.id)
    if (user!=None):
        NewCT.enable = True if user.autostartcreate == True else False
    valuechanging = "Raise 📈" if NewCT.rofl else "Fall 📉"
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}\nYou have selected: {valuechanging}", reply_markup=None)
    for item in TasksList:
        if NewCT.id == item.id:
            NewCT.id += 1
        if item.base == NewCT.base and item.quote == NewCT.quote and item.rofl == NewCT.rofl and item.user_id == NewCT.user_id :
            bot.send_message(chat_id=message.chat.id, text=f"You already have same task: {NewCT.base}/{NewCT.quote}.\n{item.ToString()}\n\You must edit or delete it!", reply_markup=keyboards.get_remove_edit_kb(item.id))
            return
    bot.send_message(chat_id=message.chat.id, 
    text=f"""Your task succesuffuly created. \nDetails of your task:
    {NewCT.ToString()}\n\nTo add new send /createtask\nTo start tasks send /turnontasks""", 
                    reply_markup=keyboards.get_starttask_keys(NewCT.id))
    TasksList.append(NewCT)
    CT.write_json_tasks(TasksList)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#Обработки call-backov 
@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def handshit(message):
    bot.send_message(chat_id=message.chat.id, text="I dont accept this. I will send it to my admin!!")
    

#Возвращает ТОЛЬКО текущую позицию таска в ЛИСТЕ (НЕ ID)
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
        global NewCT
        global TasksList
        taskz = match3.group(1)
        idz = int(match3.group(2))
        if (taskz == "settimer" or taskz == "timer"):
            set_notify_timer(message)
        idz = id_task_finder(int(match3.group(2)), message.chat.id)
        if idz == -1:
            bot.send_message(chat_id=message.chat.id, text="🚫You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
            return   
        if (taskz == "start" or taskz == "enable"):
            TasksList[idz].enable = True
            bot.send_message(chat_id=message.chat.id, text=f"✅ Pair {TasksList[idz].ToShortId()} is now monitoring!")
        elif (taskz == "disable" or taskz == "stop"):
            TasksList[idz].enable = False
            bot.send_message(chat_id=message.chat.id, text=f"❗️Monitoring disabled for {TasksList[idz].ToShortId()}")
        elif (taskz == "edittask" or taskz == "edit"):
            TasksList[idz].enable = False
            NewCT = TasksList[idz]
            echo = bot.send_message(chat_id=message.chat.id, text=f"🖍 You are editting pair: {NewCT.ToShortId()}.\nFor edit price send the new one.\nSelect price changing factor or you can set your value.", reply_markup=keyboards.get_edit_price_keyboard(idz,TasksList[idz].rofl))
            #TasksList.remove(NewCT)
            #bot.register_next_step_handler(message=echo,callback=crtask_priceset)
        elif (taskz == "remove" or taskz == "delete"):
            item = TasksList[idz]
            item.enable = False
            bot.send_message(chat_id=message.chat.id, text=f"❌ Pair ID {item.id} {item.base}/{item.quote} removed!")
            TasksList.remove(item)
            CT.write_json_tasks(TasksList)
        
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="🚫 Missing task ID", reply_markup=keyboards.get_startup_keys())



@bot.message_handler(commands=["checkprice"])
def pricecheck(message):
    echo = bot.send_message(chat_id=message.chat.id, text="To check current exchange rates send me currency pair.\n\nFor example: BTC/USDT or RVN/BTC.\nPlease observe this pattern")
    bot.register_next_step_handler(message=echo, callback=pricechecker)

def pricechecker(message):
    pairpattern = re.compile(r'(\w{2,5})/(\w{2,5})').match(message.text)
    if pairpattern != None:
        basecur = pairpattern.group(1).upper()
        quotecur = pairpattern.group(2).upper()
        if ExCuWorker.isCurrencyValid(basecur, True) and ExCuWorker.isCurrencyValid(quotecur, False):
            #pricecur = ExCuWorker.monitor(basecoin=basecur, quotecoin=quotecur)
            pricecur = ExCuWorker.bin_getCur(base=basecur, quote=quotecur)
            pricecur = pricecur if pricecur>0.001 else "{:^10.8f}".format(pricecur)
            bot.send_message(chat_id=message.chat.id ,text=f"💸Current price for pair {basecur}/{quotecur}: {pricecur}")
        else:
            bot.send_message(chat_id=message.chat.id ,text=f"I can't find pair {basecur}/{quotecur} in the list")
    else:
        bot.send_message(chat_id=message.chat.id, text="You send wrong call.\n You must observe pattern!")
    
# Не требует доработки
@bot.message_handler(commands=['turnontasks', 'startall', 'startalltasks'])
def startALLtasks(message):
    if len(TasksList) > 0:
        checkifnewuser(message)
        i = 0
        ix = 0
        for item in TasksList:
            if message.chat.id == item.user_id:
                if item.enable==False:
                    item.enable=True
                    i+=1
                else: 
                    ix += 1
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

#Need to be revorked
def removealltasks(message):
    i = 0
    count = len(TasksList)
    for i in range(count):
        if TasksList[i].user_id == message.chat.id:
            TasksList.remove(TasksList[i])
            i-=1
        else: 
            i+=1
    CT.write_json_tasks(TasksList)
    bot.send_message(chat_id=message.chat.id, text=f"Your monitoring list of {i} tasks was been destroyed!")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        global NewCT
        global TasksList
   
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        matchreEdUD = recombos.re_fast_value_change.match(call.data)
        mathretask = recombos.task_manupulation_re.match(call.data)
        edittask_re = recombos.edit_task_re.match(call.data)
        # быстрый выбор quote при создании таска (пока не используется)
        commandQuoteMatch = recombos.create_quote_kb.match(call.data)
        checkifnewuser(call.message)
        if commandQuoteMatch != None:
            NewCT.quote = commandQuoteMatch.group(1)
            expr = ExCuWorker.bin_getCur(base=NewCT.base, quote= NewCT.quote) 
            echo = bot.send_message(chat_id=call.message.chat.id, text=f"You have setted the pair: {NewCT.base}/{NewCT.quote}. Now send me the price witch you want to get (for example: '{expr}')")
            bot.register_next_step_handler(message=echo,callback=crtask_priceset)
            return
        if call.data == "CreateRaise" or call.data == "CreateFall":
            crtask_rofl(call.message, call.data)
        elif call.data == "createanyway":
            bot.send_message(chat_id=call.message.chat.id, 
            text=f"""Your task succesuffuly created. \nDetails of your task:
            {NewCT.ToString()}\n\nTo add new send /createtask\nTo start tasks send /turnontasks""", 
            reply_markup=keyboards.get_starttask_keys(NewCT.id))
            TasksList.append(NewCT)
            CT.write_json_tasks(TasksList)
        elif call.data == "createtask":
            create_task_h(call.message)
        elif call.data == "turnontasks":
            startALLtasks(call.message)
        elif call.data == "stopalltasks":
            stoptasks(call.message)
        elif call.data == "removealltasks":
            removealltasks(call.message)
        elif call.data == "viewtasks":
            showtasks(call.message)
        elif matchreEdUD != None:
            procent = int(matchreEdUD.group(2))/100
            received_id = int(matchreEdUD.group(3))
            #Сразу узнаем received_id для всех операций ниже
            RealID = id_task_finder(received_id, call.message.chat.id)
            if matchreEdUD.group(1) == "up":
                TasksList[RealID].price = TasksList[RealID].price *(1+procent)
                bot.send_message(chat_id=call.message.chat.id, text=f"☑️ Trigger moved to {TasksList[RealID].price} for {TasksList[RealID].ToShortId()}")
                return
            elif matchreEdUD.group(1) == "dn":
                TasksList[RealID].price = TasksList[RealID].price *(1-procent)
                bot.send_message(chat_id=call.message.chat.id, text=f"☑️ Trigger moved to {TasksList[RealID].price} for {TasksList[RealID].ToShortId()}")
                return
        elif edittask_re != None:
            received_id = int(edittask_re.group(1))
            RealID = id_task_finder(received_id, call.message.chat.id)
            TasksList[RealID].enable = False
            NewCT = TasksList[RealID]
            expr = ExCuWorker.bin_getCur(base=NewCT.base, quote= NewCT.quote)
            echo = bot.send_message(chat_id=call.message.chat.id, text=f"🖍 You are editting pair: {NewCT.ToShortId()}.\nFor edit price send the new one.\nFor example: {expr}")
            TasksList.remove(NewCT)
            bot.register_next_step_handler(message=echo, callback=crtask_priceset)
        #Функции ниже предназначены для обработки взаимодействий связанных с тасками напрямую  s
        elif mathretask != None:
            received_id = int(mathretask.group(2))
            #Сразу узнаем received_id для всех операций ниже
            RealID = id_task_finder(received_id, call.message.chat.id)
            if RealID == -1:
                bot.send_message(chat_id=call.message.chat.id, text="You have sent wrong task id!")
                return
            if  mathretask.group(1) == "disable":
                TasksList[RealID].enable=False
                bot.send_message(chat_id=call.message.chat.id, text="❗️Monitoring disabled for selected ID")
                CT.write_json_tasks(TasksList)
            elif mathretask.group(1) == "edittask":
                echo = bot.send_message(chat_id=call.message.chat.id, text=f"🖍 You are editting pair: {NewCT.ToShortId()}. Select price changing factor or you can set your value.", reply_markup=keyboards.get_edit_price_keyboard(TasksList[RealID].id,TasksList[RealID].rofl))
            elif mathretask.group(1) == "overridetask":
                TasksList[RealID].price = NewCT.price
                bot.send_message(chat_id=call.message.chat.id,
                text=f"Your task overrided. \nDetails of your task:\n{TasksList[RealID].ToString()}", reply_markup=keyboards.get_starttask_keys(RealID))
                CT.write_json_tasks(TasksList)
            elif mathretask.group(1) == "removetask":
                item = TasksList[RealID]
                item.enable = False
                bot.send_message(chat_id=call.message.chat.id, text=f"⭕️ Pair ID {item.id} {item.base}/{item.quote} removed!")
                TasksList.remove(item)
                CT.write_json_tasks(TasksList)
            elif mathretask.group(1) == "starttask":
                TasksList[RealID].enable = True
                bot.send_message(chat_id=call.message.chat.id, text=f"✅ Pair {TasksList[RealID].base}/{TasksList[RealID].quote} is now monitoring!") 
    except (IndexError):
        bot.send_message(chat_id=call.message.chat.id, text="🚫 Action is outdated.")  
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
def set_notify_timer(message):
    try:
        timesecs = float(message.text)
         
        user = getUSByID(message.chat.id)
        if (user!=None):
            user.notifytimer= timesecs
            bot.send_message(chat_id=message.chat.id, text=f"📣Notification delay setted on {timesecs}sec.🕒")
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="Wrong value!")    
    
@bot.message_handler(commands=['getrates'])
def getrates(message):
    printer = ""
    getcources = ExCuWorker.bin_get_monitor()
    for item in TasksList:
        if item.user_id == message.chat.id: 
            cur = ExCuWorker.bin_monitor(base=item.base, quote= item.quote, basecurses= getcources)
            printer += f"▫️ [ID #{item.id}] {item.base}/{item.quote} - {cur}\n"
    if printer!="":
        bot.send_message(chat_id=message.chat.id, text=f"📈 Your currency exchange rates, based on your tasks: 📉\n\n{printer}")
    else:
        bot.send_message(chat_id=message.chat.id, text="You didn't have any tasks", reply_markup=keyboards.get_create_only())
            
    
@bot.message_handler(commands=['showtasks', 'viewtasks', 'checktasks'])
def showtasks(message):
    checkifnewuser(message)
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
                     text=f"This bot is written on Python with pyTelegramBotApi library. This bot uses realtime binance exchange rates, and exchange rates updates every second!\n⛏ Developer: Ironshell\n🛸 Github: https://github.com/IronShell1207/CryCurMonitorBot\n\nIf bot is usefull for you, you can buy my a ☕️ and thx 2u).\n🥇ETH: 0xa35fbab442da4e65413045a4b9b147e2a0fc3e0c\n🎈LTC: LQiBdMeCNWAcSBEhc2QT3ffFz8a2t7zPcG")

@bot.message_handler(commands=['setstyle'])
def setstyle(message):
    user = getUSByID(message.chat.id)
    if (user!=None):
        user.notifystyle = not user.notifystyle
        prints = "📢 Notifications about exchange rates changes now shows separately" if user.notifystyle == False else "📢 Notifications about exchange rates changes now shows jointly in single message"
        bot.send_message(chat_id=message.chat.id, text = prints)

@bot.message_handler(func=lambda message: message.text in ["Display tasks list 📝","Create new 📊","Start all ▶️","Disable all ⏸", "Settings ⚙️","Display rates ✅"])
def msg_kb_handler(message):
    if message.text == "Display tasks list 📝":
        showtasks(message)
    elif message.text == "Create new 📊":
        create_task_h(message)
    elif message.text == "Start all ▶️":
        startALLtasks(message)
    elif message.text == "Disable all ⏸":
        stoptasks(message)
    elif message.text == "Settings ⚙️":
        user = getUSByID(message.chat.id)
        if (user!=None):
            bot.send_message(chat_id=message.chat.id, text=f"Current settings:\nNotifications delay: {user.notifytimer}\nAuto enable new tasks: {user.autostartcreate}", reply_markup=keyboards.get_settings_kb())
            return
    elif message.text == "Display rates ✅":
        getrates(message)

@bot.message_handler(func=lambda message: message.text in ["🕘Notification timeout","✅Auto enable new task"])
def settings_kb_hand(message):
    
    if message.text == "✅Auto enable new task":
        user = getUSByID(message.chat.id)
        if (user!=None):
            user.autostartcreate = not user.autostartcreate
            bot.send_message(chat_id=message.chat.id, text=f"Auto enabling new tasks active status: {user.autostartcreate}", reply_markup=keyboards.get_main_keyboard())
    elif message.text == "🕘Notification timeout":
        echo = bot.send_message(chat_id=message.chat.id, text="Send me number of seconds for notification delay (this only works for changing the delay between notifications)", reply_markup=keyboards.get_main_keyboard())
        bot.register_next_step_handler(echo, set_notify_timer)
        
    
        
@bot.message_handler(commands=['help'])
def help(message):
    echo = bot.send_message(chat_id=message.chat.id,
                            text="""Commands list:
1. Create new monitoring task - /createtask
or /createtask <base> <quote> <price> <+|-> ("+" for choose raising or "-" for falling price)
2. Start all monitoring tasks - /turnontasks
3. Stop all monitoring tasks - /stopalltasks
4. Show all tasks /showtasks
5. Disable monitoring by ID - /disable <id>
6. Start monitoring by ID - /enable <id>
7. Edit task - /edit <id>
8. Delete task /remove <id>
9. Set notification delay (seconds) - /settimer <secs>
10. Change notification style from separate messages to single - /setstyle
11. Get all current exchange rates - /getrates""")
    


def new_task_loop(message):
    try:
        while(True):
            timer_usr = 30
            lastnofity = False
            user = getUSByID(message.chat.id)
            if (user!=None):
                timer_usr = user.notifytimer
            printer = ""
            getcources = ExCuWorker.bin_get_monitor()
            for task in TasksList:
                if message.chat.id == task.user_id and task.enable == True:
                    getprice = ExCuWorker.bin_monitor(task.base, task.quote, getcources)
                    if getprice == None:
                        task.enable = False
                        bot.send_message(chat_id=message.chat.id, text= f"Something went wrong with price checking of pair {task.base}/{task.quote}")
                        continue
                    taskprice = task.price if task.price>0.0001 else "{:^10.8f}".format(task.price)
                    if task.rofl== True and getprice> taskprice:
                        printer += f"🔺 [ID {task.id}] {task.base}/{task.quote} already raise 📈 from {taskprice} to {getprice}!\n"
                    elif task.rofl == False and getprice<taskprice:
                        printer += f"🔻 [ID {task.id}] {task.base}/{task.quote} already fall 📉 from {taskprice} to {getprice}!\n"
                    else:
                        pass
            if printer == "":
                time.sleep(2.5)
            elif printer!= "":
                bot.send_message(chat_id=message.chat.id, text=f"⚠️ Your updated exchange rates list:\n{printer}\nTo edit task send: /edittask <task id>\nTo disable: /disable <task_id>")
                time.sleep(timer_usr)
    except ConnectionError as ce:
        bot.send_message(chat_id=message.chat.id,text=f"There is some problems with api connection\n{str(ce)}")
        new_task_loop(message)
    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=f"Some error occured!\n{str(e)}")
        new_task_loop(message)
        
       

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