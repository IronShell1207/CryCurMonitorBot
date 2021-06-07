from logging import makeLogRecord
import os
import threading
from typing import Counter, Text
from requests.api import get
import telebot
import json
import urllib.request
import requests
import time
import datetime

from telebot.types import Message
import config
import sys
import itertools
import datetime
import re
import subprocess
import kbuttons

import mainkb_handler as kb_handler

from Trasnlwrk import Translations as trs
import ExCuWorker
import CryptoTask as CT
import keyboards
import recombos


#TasksList = []
#Требуется создать файл config.py и добавить в него строку TOKEN="<ваш токен>"
tof = config.TOKEN if input('Choose your destiny: 1 - release, 2 - dev\n')=='1' else config.TOKEN_px
bot = telebot.TeleBot(token=tof)

commandsRE = re.compile("/(\S+)\s(\d+)")
createRE = re.compile("/(\S+)\s(\S{1,5})\s(\S{1,4})\s(\d+)\s(Fall|Raise)") #/createtask BTC USDT 56000 Raise


mainthread = threading.Thread()
#USERlist=[]

USERlist = CT.get_json_user_list()
USERlist = USERlist

TasksList = CT.get_json_task_list()


def retUser(message):
    for user in USERlist:
        if user.user_id == message.chat.id:
            return user
    print(f"Thread for {message.chat.id} created")
    NewCT = CT.CryptoTask(user_id=message.chat.id)
    user = CT.UserSets(user_id=message.chat.id, notifytimer = 80)
    USERlist.append(user)
    CT.write_json_users(USERlist)
    return user


#xa = [x for x in TasksList if x.user_id == message.chat.id]
#idxa = [x for x in TasksList if x.id == idx]


@bot.message_handler(content_types=["audio", "animation","document", "photo", "sticker", "video", "video_note","none", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'], func = lambda message: message != None)
def handshit(message):
    bot.send_message(chat_id=message.chat.id, text=trs.mg_dont_accept_err(retUser(message).language))

@bot.message_handler(content_types=['text'], func= lambda message: ('createtask' in message.text or 'create' in message.text or 'newtask' in message.text) or recombos.create_univers.match(message.text) != None)
def create_task_h(message):
    try: 
        cmb = recombos.create_univers.match(message.text)
        retUser(message).CTask = CT.CryptoTask(user_id=message.chat.id)
        if cmb != None:
            retUser(message).CTask.base = cmb.group(2).upper()
            retUser(message).CTask.quote = cmb.group(4).upper()
            retUser(message).CTask.enable = retUser(message).autostartcreate
            pr_ch = ExCuWorker.bin_getCur(retUser(message).CTask.base, retUser(message).CTask.quote)
            if pr_ch != None:
                if cmb.group(6) == None:
                    echo = bot.send_message(chat_id=message.chat.id, text=f"Pair {retUser(message).CTask.base}/{retUser(message).CTask.quote} created.\nSpecify the value you want to get for this pair.")
                    bot.register_next_step_handler(echo, crtask_priceset)
                    return
                retUser(message).CTask.price = float(cmb.group(6))
                if cmb.group(8) == None:
                    bot.send_message(chat_id=message.chat.id, text = f"Pair {retUser(message).CTask.base}/{retUser(message).CTask.quote} with value {retUser(message).CTask.price} created.\nSelect the movement of value of your pair falling or raising", reply_markup=keyboards.get_raise_fall_kb())
                    return
                retUser(message).CTask.rofl = True if cmb.group(8) == "+" or cmb.group(8) == "Raise" else False
                TasksList.append(retUser(message).CTask)
                CT.write_json_tasks(TasksList)
                bot.send_message(chat_id=message.chat.id, text = f"✅ Your monitoring task created.\n{retUser(message).CTask.ToString()}", reply_markup=keyboards.get_starttask_keys(retUser(message).CTask.id))
                return
            else:
                bot.send_message(chat_id=message.chat.id, text = f"You have sent wrong pair! Recheck your currencies")
        else:
            echo = bot.send_message(chat_id=message.chat.id, text="To create new monitoring task send me the pair witch you want to monitor.\nFirst send me base currency.\n\nExample: 'BTC' 'LTC' 'ETH' (without quotes)")
            bot.register_next_step_handler(echo, crtask_baseset)
            return
    except ValueError as ex :
        bot.send_message(chat_id=message.chat.id, text=f"Error {ex}")


def crtask_baseset(message):
    revalue = recombos.re_value_name.match(message.text)
    if revalue != None:
        retUser(message).CTask.base = message.text.upper()
        quotes_stack = ExCuWorker.bin_get_pair_quotes(retUser(message).CTask.base)
        if len(quotes_stack)>0:
            bot.send_message(chat_id=message.chat.id, text=f"📝 Task creation\n\nYour base currency: {retUser(message).CTask.base}. \nNow select quote for create pair.", reply_markup=keyboards.get_quotes_keyboard(quotes_stack))
        #bot.register_next_step_handler(message=echo, callback=crtask_quotetask)
        else:
            bot.send_message(chat_id=message.chat.id, text="🚫 Error. You have sent wrong currency name")
    else:
        bot.send_message(chat_id=message.chat.id, text="🚫 Error. You have sent wrong value")


#2-й этап   не юзается  
def crtask_quotetask(message):
    revalue = recombos.re_value_name.match(message.text)
    if revalue != None:
        retUser(message).CTask.quote = message.text.upper()
        priceex = ExCuWorker.bin_getCur(base= retUser(message).CTask.base, quote= retUser(message).CTask.quote)
        if (priceex != None):
            priceex = priceex if priceex>0.001 else "{:^10.8f}".format(priceex)
            echo = bot.send_message(chat_id= message.chat.id, text=f"Task creation.\nYour pair is {retUser(message).CTask.base}\{retUser(message).CTask.quote}.\nNow send the price, which you want to get. If exchange rates of this pair gets to this price you will get the notifications.\nExample: {priceex}")
            bot.register_next_step_handler(message=echo, callback=crtask_priceset)
        else:
            bot.send_message(chat_id=message.chat.id, text=f"🚫 Your pair is wrong. Task creation aborted")
    else:
        bot.send_message(chat_id=message.chat.id, text="🚫 Error. You have sent wrong value")


#3Й-этап (цена)
def crtask_priceset(message):
    try:
        retUser(message).CTask.price = float(str(message.text).replace(',','.'))
        echo = bot.send_message(chat_id=message.chat.id, text=f"Pair: {retUser(message).CTask.base}/{retUser(message).CTask.quote}\nPrice: {message.text}.\n📈 Should the price rise or fall to this price?", reply_markup = keyboards.get_raise_fall_kb())
    except (ValueError):
        echo = bot.send_message(chat_id=message.chat.id, text=f"❌ You have sent wrong value! Task creation aborted! Send /createtask again.", reply_markup = keyboards.get_startup_keys())

#4-й этап (создание таска)
def crtask_rofl(message, data):
    retUser(message).CTask.rofl = True if data == "CreateRaise" else False
    #retUser(message).CTask.enable = True if retUser(message).autostartcreate 
    valuechanging = "Raise 📈" if retUser(message).CTask.rofl else "Fall 📉"
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}\n\nYou have selected: {valuechanging}", reply_markup=None)
    varExist = [x for x in TasksList if x.user_id == message.chat.id and x.base == retUser(message).CTask.base and x.quote == retUser(message).CTask.quote and x.rofl == retUser(message).CTask.rofl]
    if len(varExist)>0 and varExist != None:
        bot.send_message(chat_id=message.chat.id, text=f"You already have same task: {retUser(message).CTask.base}/{retUser(message).CTask.quote}.\n{varExist[0].ToString()}\n\You must edit or delete it!", reply_markup=keyboards.get_remove_edit_kb(varExist[0].id))
        return
    TasksList.append(retUser(message).CTask)
    CT.write_json_tasks(TasksList)
    bot.send_message(chat_id=message.chat.id, 
    text=f"""✅ Your task succesuffuly created. \nDetails of your task:
    {retUser(message).CTask.ToString()}""", 
                    reply_markup=keyboards.get_starttask_keys(retUser(message).CTask.id))
    
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#Обработки call-backov 

# edit task
@bot.message_handler(content_types=['text'],func= lambda message: recombos.edit_re.match(message.text)!= None)
def edittask_handler(message):
    try:  
        match = recombos.edit_re.match(message.text)
        id = match.group(2)
        item = [x for x in TasksList if x.user_id == message.chat.id and x.id == int(id)][0]
        price = match.group(4)
        if price != None:
            item.enable = retUser(message).autostartcreate
            item.price = float(price)
            bot.send_message(chat_id=message.chat.id, text=f"Task edited! Info:\n\n{item.ToString()}")
        else:
            item.enable = False
            retUser(message).CTask = item
            bot.send_message(chat_id=message.chat.id, text=f"🖍 You are editting pair:\n{item.ToShortStr()}.\nFor edit price send the new one.\nSelect price changing factor or you can set your value.\n\nElse you can send /edit <id> <new_price> to fast edit!", reply_markup=keyboards.get_edit_price_keyboard(item.id,item.rofl,item.enable))
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text="🚫 Missing task ID.\nThe command should look like this: \n/edit <task_id> <new_price>* \n* - price is optional", reply_markup=keyboards.get_startup_keys())
        

@bot.message_handler(content_types=['text'], func= lambda message: commandsRE.match(message.text) != None)
def task_manage_handler(message):
    try:
        match3 = commandsRE.match(message.text)
        taskz = match3.group(1)
        idz = int(match3.group(2))
        if (taskz == "settimer" or taskz == "timer"):
            set_notify_timer(message)
        item = [x for x in TasksList if x.user_id == message.chat.id and x.id == idz][0]
        if item == None:
            bot.send_message(chat_id=message.chat.id, text="🚫You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
            return   
        if (taskz == "start" or taskz == "enable"):
            item.enable = True
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=message.chat.id, text=f"✅ Pair {item.ToShortId()} is now monitoring!")
        elif (taskz == "disable" or taskz == "stop"):
            item.enable = False
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=message.chat.id, text=f"❗️Monitoring disabled for {item.ToShortId()}")
        #elif (taskz == "edittask" or taskz == "edit"):
        #    item.enable = False
        #    retUser(message).CTask = item
        #    echo = bot.send_message(chat_id=message.chat.id, text=f"🖍 You are editting pair:\n{item.ToShortStr()}.\nFor edit price send the new one.\nSelect price changing factor or you can set your value.", reply_markup=keyboards.get_edit_price_keyboard(idz,item.rofl,item.enable))
        elif (taskz == "remove" or taskz == "delete"):
            item.enable = False
            bot.send_message(chat_id=message.chat.id, text=f"❌ Pair ID {item.id} {item.base}/{item.quote} removed!")
            TasksList.remove(item)
            CT.write_json_tasks(TasksList)
    except (IndexError):
        bot.send_message(chat_id=message.chat.id, text="🚫 You have sent wrong task id!", reply_markup=keyboards.get_startup_keys())
        return
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="🚫 Missing task ID", reply_markup=keyboards.get_startup_keys())


@bot.message_handler(content_types=['text'], commands=["checkprice"])
def pricecheck(message):
    echo = bot.send_message(chat_id=message.chat.id, text="To check current exchange rates send me currency pair.\n\nFor example: BTC/USDT or RVN/BTC.\nPlease observe this pattern")
    bot.register_next_step_handler(message=echo, callback=pricechecker)
  

@bot.message_handler(commands=['test'])
def test(message):
    pass
    #kbvk.send_mam(message,bot)

@bot.message_handler(content_types=['text'], func=lambda message: recombos.re_show_tasks.match(message.text)!=None)
def showtasksbyname(message):
    match = recombos.re_show_tasks.match(message.text).group(2).upper()
    tasks = [x for x in TasksList if x.base == match and x.user_id == message.chat.id]
    printer = ""
    if len(tasks)>0:
        for item in tasks:
            printer += item.ToShortStr()+"\n"
        bot.send_message(chat_id=message.chat.id, text=f"Your list with base - {match}:\n\n{printer}")
    else:
        bot.send_message(chat_id=message.chat.id, text=f"There is no tasks with base - {match}")

#check price via command
@bot.message_handler(content_types=['text'], func=lambda message: recombos.ckpr_pair_re.match(message.text)!=None)
def pricechecker(message):
    pairpattern = re.compile(r'(\w{2,5})/(\w{2,5})').match(str(message.text).split(' ')[-1]) if "price" in message.text else re.compile(r'(\w{2,5})/(\w{2,5})').match(message.text)
    if pairpattern != None:
        basecur = pairpattern.group(1).upper()
        quotecur = pairpattern.group(2).upper()
        pricecur = ExCuWorker.bin_getCur(basecur, quotecur)
        if pricecur != None:
            pricecur = pricecur if pricecur>0.001 else "{:^10.8f}".format(pricecur)
            bot.send_message(chat_id=message.chat.id ,text=f"💸Current price for pair {basecur}/{quotecur}: {pricecur}")
        else:
            bot.send_message(chat_id=message.chat.id ,text=f"I can't find pair {basecur}/{quotecur}. Recheck your writting!")
    else:
        bot.send_message(chat_id=message.chat.id, text="You send wrong call.\n You must observe pattern!")
    


@bot.message_handler(commands=['stopalltasks','stopall'])
def stoptasks(message):
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    if len(usertasks)>0:
        for task in usertasks:
            task.enable = False
        bot.send_message(chat_id=message.chat.id, text="⛔️ All tasks are stopped.")
        CT.write_json_tasks(TasksList)
    else: 
        bot.send_message(chat_id=message.chat.id, text="❌ You have not added any tasks yet! To add new send /createtask")



@bot.message_handler(commands=['turnontasks', 'startall', 'startalltasks'])
def startALLtasks(message):
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    retUser(message)
    if len(usertasks) > 0:
        ix = 0
        for task in usertasks:
            if task.enable != True:
                task.enable = True
                ix+=1
        alreadyon = f"and {len(usertasks)-ix} tasks already ON ✅" if len(usertasks)-ix>0 else ""   
        CT.write_json_tasks(TasksList)
        bot.send_message(chat_id=message.chat.id, text=f"Your {ix} monitoring tasks are started {alreadyon}\nFor check all your tasks send /showtasks")
    else: 
        bot.send_message(chat_id=message.chat.id, text="You have not added any tasks yet! To add new send /createtask")
        
        

def setnewvalue(message):
    try:
        retUser(message).CTask.price = float(message.text)
        retUser(message).CTask.enable = retUser(message).autostartcreate
        TasksList.append(retUser(message).CTask)
        CT.write_json_tasks(TasksList)
        bot.send_message(chat_id=message.chat.id, text=f"Task edited! Info:\n\n{retUser(message).CTask.ToString()}")
    except ValueError as ex:
        bot.send_message(chat_id=message.chat.id, text='❌ You have sent wrong value')
        TasksList.append(retUser(message).CTask)
        

def removealltasks(message):
    bot.send_message(chat_id=message.chat.id, text=f"Your monitoring list has been fully removed\nand you have been banned!\n❌❌❌📛📛📛❌❌❌\nJust kidding")
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    for taskus in usertasks:
        TasksList.remove(taskus)     
    CT.write_json_tasks(TasksList)
    


#Обработка быстрого изменения таска (через кнопки)
@bot.callback_query_handler(func=lambda call: True and recombos.re_fast_value_change.match(call.data)!= None)
def callback_fastChangeValue(call):
    try:
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        match = recombos.re_fast_value_change.match(call.data)
        procent = int(match.group(2))/100
        r_id = int(match.group(3))
        task = [x for x in TasksList if call.message.chat.id == x.user_id and x.id == r_id][0]
        old_pr = task.price
        task.price = task.price* (1+procent) if match.group(1) == "up" else task.price* (1-procent)
        task.price = round(task.price,3) if task.price>0.001 else task.price 
        pr = float("{:^10.2f}".format(task.price)) if task.price>0.001 else float("{:^10.8f}".format(task.price))  
        task.enable = True
        CT.write_json_tasks(TasksList)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}\n\n☑️ Trigger moved from {old_pr} to {pr} for {task.ToShortId()}", reply_markup=None)
    except (IndexError):
        bot.send_message(chat_id=call.message.chat.id, text="🚫 Action is outdated.")


#Обработка манипуляциями с заданиями (старт, стоп, изм...)
@bot.callback_query_handler(func=lambda call: True and recombos.task_manupulation_re.match(call.data))
def callback_taskchanger(call):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        match = recombos.task_manupulation_re.match(call.data)
        r_id = int(match.group(2))
        r_task = match.group(1)
        task = [x for x in TasksList if call.message.chat.id == x.user_id and x.id == r_id][0]
        if r_task == "starttask":
            task.enable = True
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=call.message.chat.id, text=f"✅ Pair {task.base}/{task.quote} is now monitoring!") 
        elif r_task == "newv":
            retUser(call.message).CTask = task
            TasksList.remove(task)
            echo = bot.send_message(chat_id=call.message.chat.id, text=f"To set a new value for pair {task.ToShortStr()} send it in next message")
            bot.register_next_step_handler(echo, callback=setnewvalue)
        elif r_task == "disable":
            task.enable = False
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=call.message.chat.id, text=f"Monitoring of {task.ToShortId()} disabled")
        elif r_task == "edittask":
            bot.send_message(chat_id=call.message.chat.id, 
                                    text=f"🖍 You are editting pair: {task.ToShortStr()}.\n Select price changing factor or you can set your value.", 
                                    reply_markup=keyboards.get_edit_price_keyboard(task.id,task.rofl,task.enable))
        elif r_task == "overridetask":
            task.price = retUser(call.message).CTask.price
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=call.message.chat.id,
                text=f"Your task overrided. \nDetails of your task:\n{task.ToString()}", reply_markup=keyboards.get_starttask_keys(r_id))
            CT.write_json_tasks(TasksList)
        elif r_task == "removetask":
            bot.send_message(chat_id=call.message.chat.id, text=f"❌ Pair ID {task.id} {task.base}/{task.quote} removed!")
            TasksList.remove(task)
            CT.write_json_tasks(TasksList)
    except IndexError as exx:
        bot.send_message(chat_id=call.message.chat.id, text=f"🚫 Action is outdated. {exx}")
    
#Обработка кнопок quote    
@bot.callback_query_handler(func=lambda call: True and recombos.create_quote_kb.match(call.data)!= None)
def callback_create_task_quote(call):
    try:
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        match = recombos.create_quote_kb.match(call.data)
        retUser(call.message).CTask.quote = match.group(1)
        #expr = ExCuWorker.bin_getCur(base=retUser(call.message).CTask.base, quote= retUser(call.message).CTask.quote) 
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=f"📝 Task creation\n\n▶️ Your pair: {retUser(call.message).CTask.base}/{retUser(call.message).CTask.quote}.\nNow tell me the price to be reached\n(for example: '0.05', '1200', '0.000002' without quotes)\nWhen this price is reached, an alert will be sent")
        bot.register_next_step_handler(message=call.message,callback=crtask_priceset)
    except Exception as es:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text=f"{call.message.text}\n\n🚫Action outdated!")
    
#Все остальные команды
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        if call.data == "CreateRaise" or call.data == "CreateFall":
            crtask_rofl(call.message, call.data)
        elif call.data == "createanyway":
            bot.send_message(chat_id=call.message.chat.id, 
            text=f"""Your task succesuffuly created. \nDetails of your task:
            {retUser(call.message).CTask.ToString()}\n\nTo add new send /createtask\nTo start tasks send /turnontasks""", 
            reply_markup=keyboards.get_starttask_keys(retUser(call.message).CTask.id))
            TasksList.append(retUser(call.message).CTask)
            CT.write_json_tasks(TasksList)
        elif call.data == "createtask":
            create_task_h(call.message)
        elif call.data == "turnontasks":
            startALLtasks(call.message)
        elif call.data == "stopalltasks":
            stoptasks(call.message)
        elif call.data == "removealltasks":
            removealltasks(call.message)
        elif call.data == "removetasksqu":
            bot.send_message(chat_id=call.message.chat.id, text="❌ Are you sure you want to clear the tracking list?\nAction cannot be undone", reply_markup=keyboards.get_remove_cfrm())
        elif call.data == "viewtasks":
            showtasks(call.message)
    except (ValueError):
        bot.send_message(chat_id=call.message.chat.id, text="🚫 Action is outdated.")  
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
def set_notify_timer(message):
    try:
        timesecs = float(message.text)
        user = retUser(message)
        user.notifytimer= timesecs
        bot.send_message(chat_id=message.chat.id, text=f"📣Notification delay setted on {timesecs}sec.🕒")
        CT.write_json_users(USERlist)
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text="Wrong value!")    
    
@bot.message_handler(commands=['getrates'])
def getrates(message):
    printer = ""
    getcources = ExCuWorker.bin_get_monitor()
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    for item in usertasks:
        cur = ExCuWorker.bin_monitor(base=item.base, quote= item.quote, basecurses= getcources)
        printer += f"▫️ [ID #{item.id}] {item.base}/{item.quote} - {cur}\n"
    if printer!="":
        bot.send_message(chat_id=message.chat.id, text=f"📈 Your currency exchange rates, based on your tasks: 📉\n\n{printer}")
    else:
        bot.send_message(chat_id=message.chat.id, text="You didn't have any tasks", reply_markup=keyboards.get_create_only())
            
    
@bot.message_handler(commands=['showtasks', 'viewtasks', 'checktasks'])
def showtasks(message):
    #   checkifnewuser(message)
    printer = ""
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    for item in usertasks:
        printer += item.ToShortStr()+"\n"
    bot.send_message(chat_id=message.chat.id, text=f"Your monitoring task list:\n\n{printer}\nTo get filtred list by base send: /show <base currency>", reply_markup=keyboards.get_en_dis_all_keys(retUser(message).language))
    
    
@bot.message_handler(commands=['start'])
def start(message):
    echo = bot.send_message(chat_id=message.chat.id, 
    text="Hello! I'm crypto currency exchange monitor bot. I can send you 💬 notification when your currency is raise 📉 or fall 📈 to setted value 💰. \nFor create new task 🖍 send: /createtask.\nFor get info 📋 send: /info\nFor get all available commands 🔎 send: /help",
    reply_markup=keyboards.get_main_keyboard(retUser(message).language))

@bot.message_handler(commands=['info'])
def infohelp(message):
    bot.send_message(chat_id=message.chat.id, 
                     text=f"This bot is written on Python with pyTelegramBotApi library. This bot uses realtime binance exchange rates, and exchange rates updates every second!\n⛏ Developer: Ironshell\n🛸 Github: https://github.com/IronShell1207/CryCurMonitorBot\n\nIf bot is usefull for you, you can buy my a ☕️ and thx 2u).\n🥇ETH: 0xa35fbab442da4e65413045a4b9b147e2a0fc3e0c\n🎈LTC: LQiBdMeCNWAcSBEhc2QT3ffFz8a2t7zPcG")

#Временно не работает
#@bot.message_handler(commands=['setstyle'])
def setstyle(message):
    user = retUser(message)
    user.notifystyle = not user.notifystyle
    prints = "📢 Notifications about exchange rates changes now shows separately" if user.notifystyle == False else "📢 Notifications about exchange rates changes now shows jointly in single message"
    bot.send_message(chat_id=message.chat.id, text = prints)




@bot.message_handler(content_types=['text'], func=lambda message: message.text in kbuttons.get_main_kb_buttons(retUser(message).language))
def msg_kb_handler(message):
    lng = retUser(message).language
    if message.text == kbuttons.display_tasks(lng):
        showtasks(message)
    elif message.text == kbuttons.create_new_task(lng):
        create_task_h(message)
    elif message.text == kbuttons.start_all_tasks_btn(lng):
        startALLtasks(message)
    elif message.text == kbuttons.disable_all_tasks_btn(lng):
        stoptasks(message)
    elif message.text == kbuttons.settings(lng):
        user = retUser(message)
        bot.send_message(chat_id=message.chat.id, text=f"Current settings:\nNotifications delay: {user.notifytimer}\nAuto enable new tasks: {user.autostartcreate}", reply_markup=keyboards.get_settings_kb(retUser(message).language))
        return
    elif message.text == kbuttons.display_rates(lng):
        getrates(message)

#клавиатура настроек
@bot.message_handler(content_types=['text'], func=lambda message: message.text in kbuttons.bottom_kb_settings(retUser(message).language)) #["🕘Notification timeout","✅Auto enable new task","◀️ Back","📝Show edit buttons","⛔️ Disable task after trigger"])
def settings_kb_hand(message):
    if message.text == kbuttons.auto_enable_not(retUser(message).language):
        user = retUser(message)
        user.autostartcreate = not user.autostartcreate
        CT.write_json_users(USERlist)
        bot.send_message(chat_id=message.chat.id, text=f"Auto enabling new tasks active status: {user.autostartcreate}", reply_markup=keyboards.get_main_keyboard(retUser(message).language))
    elif message.text == kbuttons.notify_timeout(retUser(message).language):
        echo = bot.send_message(chat_id=message.chat.id, text="Send me number of seconds for notification delay (this only works for changing the delay between notifications)", reply_markup=keyboards.get_main_keyboard(retUser(message).language))
        bot.register_next_step_handler(echo, set_notify_timer)
    elif message.text == kbuttons.back_sets_btn(retUser(message).language):
        bot.send_message(chat_id=message.chat.id, text="Settings have been closed!", reply_markup=keyboards.get_main_keyboard(retUser(message).language))
    elif message.text == kbuttons.show_edit_btns(retUser(message).language):
        retUser(message).fasteditbtns = not retUser(message).fasteditbtns
        pr = "displaying! ✅"  if retUser(message).fasteditbtns else "hidden! ❌"
        CT.write_json_users(USERlist)
        bot.send_message(chat_id=message.chat.id, text=f"⚠️ Fast edit buttons now {pr}.", reply_markup=keyboards.get_main_keyboard(retUser(message).language))
    elif message.text == kbuttons.auto_disable_task(retUser(message).language):
        retUser(message).notifyonce = not retUser(message).notifyonce 
        CT.write_json_users(USERlist)
        reta = "once" if retUser(message).notifyonce else "every time"
        bot.send_message(chat_id=message.chat.id, text=f"Now task notifications will be triggered {reta}", reply_markup=keyboards.get_main_keyboard(retUser(message).language))
    elif message.text == kbuttons.language_set(retUser(message).language):
        retUser(message).language = "rus" if retUser(message).language == "eng" else "eng"
        bot.send_message(chat_id=message.chat.id, text="Русский язык включен", reply_markup=keyboards.get_settings_kb(retUser(message).language))
    
        
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
11. Get all current exchange rates - /getrates
12. Show tasks by base currency name - /show <base>""")
    


def new_task_loop():
    try:
        date = datetime.datetime.now()
        prdate = date.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{prdate} - Thread created")
        while(True):
            time.sleep(1)
            getcources = ExCuWorker.bin_get_monitor()
            for user in USERlist:
                #print(f"{user.user_id} updating noficications")
                timer_usr = user.notifytimer
                datnow = datetime.datetime.now()
                if user.lastnotify<=datnow-datetime.timedelta(seconds=timer_usr):
                    printer = ""
                    kbfastedititems = []
                    usertasks = [x for x in TasksList if user.user_id == x.user_id and x.enable == True]
                    for task in usertasks:
                        getprice = ExCuWorker.bin_monitor(task.base, task.quote, getcources)
                        if getprice == None:
                            task.enable = False
                            bot.send_message(chat_id=user.user_id, text= f"Something went wrong with price checking of pair {task.base}/{task.quote}")
                            continue
                        taskprice = task.price if task.price>0.0001 else "{:^10.8f}".format(task.price)
                        if task.rofl== True and getprice > task.price:
                            kbfastedititems.append(task)
                            task.enable = task.enable if user.notifyonce == False else False
                            printer += f"🔺 [ID {task.id}] {task.base}/{task.quote} already raise 📈 from {taskprice} to {getprice}!\n"           
                        elif task.rofl == False and getprice < taskprice:
                            kbfastedititems.append(task)
                            task.enable = task.enable if user.notifyonce == False else False
                            printer += f"🔻 [ID {task.id}] {task.base}/{task.quote} already fall 📉 from {taskprice} to {getprice}!\n" 
                        else:
                            pass
                    if printer == "":
                        time.sleep(1.5)
                    elif printer!= "":
                        rekb = keyboards.get_fast_edit_kb(kbfastedititems) if user.fasteditbtns else None
                        bot.send_message(chat_id=user.user_id, text=f"⚠️ Your updated exchange rates list:\n{printer}\nTo edit task send: /edittask <task id>\nTo disable: /disable <task_id>",reply_markup=rekb)
                        user.lastnotify = datetime.datetime.now()
                        #time.sleep(timer_usr)
                else:
                    continue   
            time.sleep(0)
    except ConnectionError as ce:
        #bot.send_message(chat_id=user.user_id,text=f"There is some problems with api connection\n{str(ce)}")
        print(f"{datetime.datetime.now()} There is some problems with api connection\n{str(ce)}")
        
        new_task_loop()
    except Exception as e:
        print(f"{datetime.datetime.now()} Some error occured!\n{str(e)}")
        #bot.send_message(chat_id=user.user_id, text=f"Some error occured!\n{str(e)}")
        new_task_loop()
              

def main_loop():
    try:
        Binf = str(bot.get_me()).replace("'",'"').replace('None','"None"').replace('False','"False"').replace('True','"True"')
        botinfo = json.loads(Binf)
        print(f"Bot have been started. \nID: {botinfo['id']}\nName: {botinfo['first_name']}\nUserName: {botinfo['username']} ")
        mainthread = threading.Thread(target=new_task_loop)#,args=[message])
        mainthread.start()
        bot.polling(none_stop=True) 
    except ConnectionError:
        time.sleep(5)
        main_loop()
    #except TypeError as ex:
    #    print(ex)

    
if (__name__=="__main__"):
    try:
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr+ '\nExiting by user request\n')
        sys.exit(0)

#https://rest.coinapi.io/v1/exchangerate/LTC/USDT?apikey=35A30795-914A-447C-9238-9265B9DB55C4
#https://docs.coinapi.io/#endpoints-2
#https://rest.coinapi.io/v1/exchangerate/BTC?apikey=35A30795-914A-447C-9238-9265B9DB55C4