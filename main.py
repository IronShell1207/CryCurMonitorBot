from logging import makeLogRecord
import os
import threading
from typing import Counter, Text
from requests.api import get
from requests.sessions import merge_setting
import telebot
import json
import urllib.request
import requests
import time
import datetime
from telebot.apihelper import RETRY_ON_ERROR

from telebot.types import Message
import config
import sys
import itertools
import datetime
import re
import subprocess 
from Translations import settingskb, msg, mainkb, msg_sets, msg_tasks
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

USERlist = CT.get_json_user_list()
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


@bot.message_handler(content_types=["audio", "animation","document", "photo", "sticker", "video", "video_note","none", "voice", "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'], func = lambda message: message != None)
def handshit(message):
    bot.send_message(chat_id=message.chat.id, text=msg.mg_dont_accept_err(retUser(message).language))

@bot.message_handler(content_types=['text'], func= lambda message: ('createtask' in message.text or 'create' in message.text or 'newtask' in message.text) or recombos.create_univers.match(message.text) != None)
def create_task_h(message):
    user = retUser(message)
    try: 
        cmb = recombos.create_univers.match(message.text)
        user.CTask = CT.CryptoTask(user_id=message.chat.id)
        if cmb != None:
            user.CTask.base = cmb.group(2).upper()
            user.CTask.quote = cmb.group(4).upper()
            user.CTask.enable = user.autostartcreate
            pr_ch = ExCuWorker.bin_getCur(user.CTask.base, user.CTask.quote)
            if pr_ch != None:
                if cmb.group(6) == None:
                    echo = bot.send_message(chat_id=message.chat.id, text=msg_tasks.created_task_without_price(user.language,user.CTask.base,user.CTask.quote))
                    bot.register_next_step_handler(echo, crtask_priceset)
                    return
                user.CTask.price = float(cmb.group(6))
                if cmb.group(8) == None:
                    if user.autorofl == True:
                        user.CTask.rofl = True if user.CTask.price > pr_ch else False
                    else:
                        bot.send_message(chat_id=message.chat.id, 
                                        text = msg_tasks.created_task_without_rofl(user.language, 
                                                                                    user.CTask.base,
                                                                                    user.CTask.quote, 
                                                                                    user.CTask.price), 
                                        reply_markup=keyboards.get_raise_fall_kb(user.language))
                        return #f"Pair {retUser(message).CTask.base}/{retUser(message).CTask.quote} with value {retUser(message).CTask.price} created.\nSelect the movement of value of your pair falling or raising"
                else:
                    user.CTask.rofl = True if cmb.group(8) == "+" or cmb.group(8) == "Raise" else False
                task_user_add(message)
                return
            else:
                bot.send_message(chat_id=message.chat.id, text = msg_tasks.created_task_error_pair(user.language))
        else:
            echo = bot.send_message(chat_id=message.chat.id, text=msg_tasks.created_task_command_only(user.language))
            bot.register_next_step_handler(echo, crtask_baseset)
            return
    except ValueError as ex :
        bot.send_message(chat_id=message.chat.id, text=f"Error {ex}")


def get_auto_rofl(base, quote, price):
    prc = ExCuWorker.bin_getCur(base,quote)
    return True if price>prc else False

def crtask_baseset(message):
    revalue = recombos.re_value_name.match(message.text.upper())
    rev = recombos.pair_re.match(message.text.upper())
    if revalue != None and rev == None:
        retUser(message).CTask.base = message.text.upper()
        quotes_stack = ExCuWorker.bin_get_pair_quotes(retUser(message).CTask.base)
        if len(quotes_stack)>0:
            bot.send_message(chat_id=message.chat.id, 
                             text=msg_tasks.creation_base_setted(retUser(message).language, retUser(message).CTask.base), 
                             reply_markup=keyboards.get_quotes_keyboard(quotes_stack))
            return 
        else:
            bot.send_message(chat_id=message.chat.id, text=msg_tasks.creation_base_error(retUser(message).language), reply_markup=keyboards.get_create_only(retUser(message).language))
            return
    
    if rev != None:
        retUser(message).CTask.base = rev.group(1)
        retUser(message).CTask.quote = rev.group(2)
        echo = bot.send_message(chat_id=message.chat.id, 
                             text=msg_tasks.created_task_without_price(retUser(message).language, retUser(message).CTask.base, retUser(message).CTask.quote))
        bot.register_next_step_handler(message=echo, callback=crtask_priceset)
        return
    else:
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.creation_base_error(retUser(message).language), reply_markup=keyboards.get_create_only(retUser(message).language))


# Добавление задания!
def task_user_add(message):
    user = retUser(message)
    user.CTask.enable = user.autostartcreate
    TasksList.append(user.CTask)
    CT.write_json_tasks(TasksList)
    bot.send_message(chat_id=message.chat.id, 
                    text=msg_tasks.created_task_fully(user.language, user.CTask), 
                    reply_markup=keyboards.get_starttask_keys(user.language, user.CTask.id))
    pass

"""
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
"""

#3Й-этап (цена)
def crtask_priceset(message):
    try:
        user = retUser(message)
        user.CTask.price = float(str(message.text).replace(',','.'))
        if user.autorofl == True:
            pricenow = ExCuWorker.bin_getCur(user.CTask.base, user.CTask.quote)
            user.CTask.rofl = True if pricenow < user.CTask.price else False
            task_user_add(message)
        else:
            echo = bot.send_message(chat_id=message.chat.id, text=msg_tasks.creation_price_setted(retUser(message).language, retUser(message).CTask), reply_markup = keyboards.get_raise_fall_kb(retUser(message).language))
    except (ValueError):
        echo = bot.send_message(chat_id=message.chat.id, text=msg_tasks.creation_price_error(retUser(message).language), reply_markup = keyboards.get_startup_keys(retUser(message).language))

#4-й этап (создание таска)
def crtask_rofl(message, data):
    retUser(message).CTask.rofl = True if data == "CreateRaise" else False
    #retUser(message).CTask.enable = True if retUser(message).autostartcreate 
    valuechanging = "Raise 📈" if retUser(message).CTask.rofl else "Fall 📉"
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"{message.text}\n\n{msg_tasks.creation_selected(retUser(message).language)} {valuechanging}", reply_markup=None)
    varExist = [x for x in TasksList if x.user_id == message.chat.id and x.base == retUser(message).CTask.base and x.quote == retUser(message).CTask.quote and x.rofl == retUser(message).CTask.rofl]
    if len(varExist)>0 and varExist != None:
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.creation_final_already_have(retUser(message).language,retUser(message).CTask,varExist[0]), reply_markup=keyboards.get_remove_edit_kb(retUser(message).language, varExist[0].id))
        return
    task_user_add(message)
    
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
            bot.send_message(chat_id=message.chat.id, text=msg_tasks.edited_task_info(retUser(message).language, item))
        else:
            item.enable = False
            retUser(message).CTask = item
            bot.send_message(chat_id=message.chat.id, text=msg_tasks.editting_task(retUser(message).language,item), reply_markup=keyboards.get_edit_price_keyboard(retUser(message).language,item.id,item.rofl,item.enable))
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.editting_task_error(retUser(message).language), reply_markup=keyboards.get_startup_keys(retUser(message).language))
        

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
            bot.send_message(chat_id=message.chat.id, text=msg_tasks.id_error(retUser(message).language), reply_markup=keyboards.get_startup_keys(retUser(message).language))
            return   
        if (taskz == "start" or taskz == "enable"):
            item.enable = True
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=message.chat.id, text=msg_tasks.pair_monitoring_enabled(retUser(message).language, item))
        elif (taskz == "disable" or taskz == "stop"):
            item.enable = False
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=message.chat.id, text=msg_tasks.pair_monitoring_disabled(retUser(message).language, item))
        elif (taskz == "remove" or taskz == "delete"):
            item.enable = False
            TasksList.remove(item)
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=message.chat.id, text=msg_tasks.pair_removed(retUser(message).language, item))
    except (IndexError):
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.id_error(retUser(message).language), reply_markup=keyboards.get_startup_keys(retUser(message).language))
        return
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.id_error(retUser(message).language), reply_markup=keyboards.get_startup_keys(retUser(message).language))


@bot.message_handler(content_types=['text'], commands=["checkprice"])
def pricecheck(message):
    echo = bot.send_message(chat_id=message.chat.id, text=msg_tasks.check_price(retUser(message).language))
    bot.register_next_step_handler(message=echo, callback=pricechecker)
  

@bot.message_handler(content_types=['text'], func=lambda message: recombos.re_show_tasks.match(message.text)!=None)
def showtasksbyname(message):
    match = recombos.re_show_tasks.match(message.text).group(2).upper()
    tasks = [x for x in TasksList if x.base == match and x.user_id == message.chat.id]
    printer = ""
    if len(tasks)>0:
        for item in tasks:
            printer += item.ToShortStr()+"\n"
        bot.send_message(chat_id=message.chat.id, text=f"{msg_tasks.show_by_task_name(retUser(message).language)}{match}:\n\n{printer}")
    else:
        bot.send_message(chat_id=message.chat.id, text=f"{msg_tasks.show_by_task_name_err(retUser(message).language)}{match}")

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
            bot.send_message(chat_id=message.chat.id ,text=f"{msg_tasks.current_price_pair(retUser(message).language)}{basecur}/{quotecur}: {pricecur}")
        else:
            bot.send_message(chat_id=message.chat.id ,text=msg_tasks.wrong_pair(retUser(message).language,basecur,quotecur))
    else:
        bot.send_message(chat_id=message.chat.id, text="You send wrong call.\n You must observe pattern!")
    


@bot.message_handler(commands=['stopalltasks','stopall'])
def stoptasks(message):
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    if len(usertasks)>0:
        for task in usertasks:
            task.enable = False
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.stop_all_tasks(retUser(message).language))
        CT.write_json_tasks(TasksList)
    else: 
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.no_tasks_detected(retUser(message).language), reply_markup=keyboards.get_create_only(retUser(message).language))



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
        alreadyon = len(usertasks)   
        CT.write_json_tasks(TasksList)
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.start_all_tasks(retUser(message).language,ix, alreadyon))
    else: 
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.no_tasks_detected(retUser(message).language), reply_markup=keyboards.get_create_only(retUser(message).language))
        
        

def setnewvalue(message):
    try:
        user = retUser(message)
        user.CTask.price = float(message.text)
        user.CTask.enable = user.autostartcreate
        TasksList.append(user.CTask)
        CT.write_json_tasks(TasksList)
        bot.send_message(chat_id=message.chat.id, text=f"{msg_tasks.editted_task_info(user.language)}{retUser(message).CTask.ToString(user.language)}")
    except ValueError as ex:
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.wrong_value_error(user.language))
        TasksList.append(user.CTask)
        

def removealltasks(message):
    bot.send_message(chat_id=message.chat.id, text=msg_tasks.all_tasks_removed(retUser(message).language), reply_markup=keyboards.get_create_only())
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
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}{msg_tasks.trigger_moved(retUser(call.message).language,old_pr,pr,task)}", reply_markup=None)
    except (IndexError):
        bot.send_message(chat_id=call.message.chat.id, text=msg_tasks.action_outdated(retUser(call.message).language))


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
            bot.send_message(chat_id=call.message.chat.id, text=msg_tasks.pair_monitoring_enabled(retUser(call.message).language,task)) 
        elif r_task == "newv":
            retUser(call.message).CTask = task
            TasksList.remove(task)
            echo = bot.send_message(chat_id=call.message.chat.id, text=msg_tasks.new_value_set(retUser(call.message).language, task))
            bot.register_next_step_handler(echo, callback=setnewvalue)
        elif r_task == "disable":
            task.enable = False
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=call.message.chat.id, text=msg_tasks.pair_monitoring_disabled(retUser(call.message).language,task))
        elif r_task == "edittask":
            bot.send_message(chat_id=call.message.chat.id, 
                                    text=msg_tasks.task_edit_request(retUser(call.message).language, task), 
                                    reply_markup=keyboards.get_edit_price_keyboard(retUser(call.message).language,task.id,task.rofl,task.enable))
        elif r_task == "overridetask":
            task.price = retUser(call.message).CTask.price
            CT.write_json_tasks(TasksList)
            bot.send_message(chat_id=call.message.chat.id,
                text=msg_tasks.task_new_override(retUser(call.message).language, task), reply_markup=keyboards.get_starttask_keys(retUser(call.message).language,r_id))
            CT.write_json_tasks(TasksList)
        elif r_task == "removetask":
            bot.send_message(chat_id=call.message.chat.id, text=msg_tasks.pair_removed(retUser(call.message).language,task))
            TasksList.remove(task)
            CT.write_json_tasks(TasksList)
    except IndexError as exx:
        bot.send_message(chat_id=call.message.chat.id, text=f"{msg_tasks.action_outdated(retUser(call.message).language)} {exx}")
    
#Обработка кнопок quote    
@bot.callback_query_handler(func=lambda call: True and recombos.create_quote_kb.match(call.data)!= None)
def callback_create_task_quote(call):
    try:
        #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        match = recombos.create_quote_kb.match(call.data)
        retUser(call.message).CTask.quote = match.group(1)
        #expr = ExCuWorker.bin_getCur(base=retUser(call.message).CTask.base, quote= retUser(call.message).CTask.quote) 
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=msg_tasks.creation_quote_setted(retUser(call.message).language, retUser(call.message).CTask))
        bot.register_next_step_handler(message=call.message,callback=crtask_priceset)
    except Exception as es:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text=f"{call.message.text}\n\n{msg_tasks.action_outdated(retUser(call.message).language)}")
    
#Все остальные команды
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{call.message.text}", reply_markup=None)
        if call.data == "CreateRaise" or call.data == "CreateFall":
            crtask_rofl(call.message, call.data)
        elif call.data == "createanyway":
            bot.send_message(chat_id=call.message.chat.id, 
            text=msg_tasks.created_task_fully(retUser(call.message).language, retUser(call.message).CTask), 
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
            bot.send_message(chat_id=call.message.chat.id, text=msg_tasks.clear_tasks_list_request(retUser(call.message).language), reply_markup=keyboards.get_remove_cfrm(retUser(call.message).language))
        elif call.data == "viewtasks":
            showtasks(call.message)
    except (ValueError):
        bot.send_message(chat_id=call.message.chat.id, text=msg_tasks.action_outdated(retUser(call.message).language))  
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
def set_notify_timer(message):
    try:
        timesecs = float(message.text)
        user = retUser(message)
        user.notifytimer= timesecs
        bot.send_message(chat_id=message.chat.id, text=msg_sets.notify_timer(retUser(message).language,timesecs))
        CT.write_json_users(USERlist)
    except (ValueError):
        bot.send_message(chat_id=message.chat.id, text=msg_sets.wrong_value(retUser(message).language))    
    
@bot.message_handler(commands=['getrates'])
def getrates(message):
    printer = ""
    getcources = ExCuWorker.bin_get_monitor()
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    for item in usertasks:
        cur = ExCuWorker.bin_monitor(base=item.base, quote= item.quote, basecurses= getcources)
        printer += f"▫️ [ID #{item.id}] {item.base}/{item.quote} - {cur}\n"
    if printer!="":
        bot.send_message(chat_id=message.chat.id, text=f"{msg_tasks.return_rates_tasks(retUser(message).language)}{printer}")
    else:
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.no_tasks_detected(retUser(message).language), reply_markup=keyboards.get_create_only(retUser(message).language))
            
    
@bot.message_handler(commands=['showtasks', 'viewtasks', 'checktasks'])
def showtasks(message):
    printer = ""
    usertasks = [x for x in TasksList if message.chat.id == x.user_id]
    for item in usertasks:
        printer += item.ToShortStr()+"\n"
    if len(usertasks)>0:
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.return_monitoring_list(retUser(message).language,printer, retUser(message).hidehint), reply_markup=keyboards.get_en_dis_all_keys(retUser(message).language))
    else:
        bot.send_message(chat_id=message.chat.id, 
        text=msg_tasks.no_tasks_detected(retUser(message).language), reply_markup=keyboards.get_create_only(retUser(message).language))
    
@bot.message_handler(commands=['start'])
def start(message):
    usr_ex = [x for x in USERlist if message.chat.id == x.user_id]
    reply_kb = keyboards.get_language_keyboard() if len(usr_ex)==0 or usr_ex == None else keyboards.get_main_keyboard(retUser(message).language)
    new_user = True if len(usr_ex)==0 or usr_ex == None else False
    if not new_user:
        echo = bot.send_message(chat_id=message.chat.id, 
    text=f"{msg_tasks.info_start(retUser(message).language)}",
    reply_markup=reply_kb)
    else:
        gif = open('mp4.mp4', 'rb')
        bot.send_animation(chat_id=message.chat.id, animation=gif)
        bot.send_message(chat_id=message.chat.id, text=f"Hello! Please select your language by clicking on the button below to continue!", reply_markup=keyboards.get_language_keyboard())

@bot.message_handler(commands=['info'])
def infohelp(message):
    bot.send_message(chat_id=message.chat.id, 
                     text=msg_tasks.info_bot(retUser(message).language))

#Временно не работает
#@bot.message_handler(commands=['setstyle'])
def setstyle(message):
    user = retUser(message)
    user.notifystyle = not user.notifystyle
    prints = "📢 Notifications about exchange rates changes now shows separately" if user.notifystyle == False else "📢 Notifications about exchange rates changes now shows jointly in single message"
    bot.send_message(chat_id=message.chat.id, text = prints)




@bot.message_handler(content_types=['text'], func=lambda message: message.text in mainkb.get_main_kb_buttons(retUser(message).language))
def msg_kb_handler(message):
    if message.text == mainkb.display_tasks("rus") or message.text == mainkb.display_tasks("eng"):
        showtasks(message)
    elif message.text == mainkb.create_new_task("rus") or message.text == mainkb.create_new_task("eng"):
        create_task_h(message)
    elif message.text == mainkb.start_all_tasks_btn("rus") or message.text == mainkb.start_all_tasks_btn("eng"):
        startALLtasks(message)
    elif message.text == mainkb.disable_all_tasks_btn("rus") or message.text == mainkb.disable_all_tasks_btn("eng"):
        stoptasks(message)
    elif message.text == mainkb.settings("rus") or message.text == mainkb.settings("eng"):
        user = retUser(message)
        bot.send_message(chat_id=message.chat.id, text=msg_sets.current_sets(retUser(message)), reply_markup=keyboards.get_settings_kb(retUser(message).language))
        return
    elif message.text == mainkb.display_rates("rus") or  message.text == mainkb.display_rates("eng"):
        getrates(message)

#клавиатура настроек
@bot.message_handler(content_types=['text'], func=lambda message: message.text in settingskb.bottom_kb_settings(retUser(message).language))
def settings_kb_hand(message):
    user = retUser(message)
    if message.text == settingskb.auto_enable_not("rus") or message.text == settingskb.auto_enable_not("eng"):
        user.autostartcreate = not user.autostartcreate
        CT.write_json_users(USERlist)
        bot.send_message(chat_id=message.chat.id, text=str.format(msg_sets.autoenable_message(user.language),user.autostartcreate),reply_markup=keyboards.get_main_keyboard(user.language))
        #7bot.send_message(chat_id=message.chat.id, text=f"Auto enabling new tasks active status: {user.autostartcreate}", reply_markup=keyboards.get_main_keyboard(retUser(message).language))
    elif message.text == settingskb.notify_timeout("rus") or message.text == settingskb.notify_timeout("eng"):
        echo = bot.send_message(chat_id=message.chat.id, text=msg_sets.notification_delay_set(user.language), reply_markup=keyboards.get_main_keyboard(user.language))
        bot.register_next_step_handler(echo, set_notify_timer)
    elif message.text == settingskb.back_sets_btn("rus") or message.text == settingskb.back_sets_btn("eng"):
        bot.send_message(chat_id=message.chat.id, text=msg_sets.close_setting_menu(user.language), reply_markup=keyboards.get_main_keyboard(user.language))
    elif message.text == settingskb.show_edit_btns("rus") or message.text == settingskb.show_edit_btns("eng"):
        user.fasteditbtns = not user.fasteditbtns
        CT.write_json_users(USERlist)
        bot.send_message(chat_id=message.chat.id, text=msg_sets.fastEditBtns_txt(user.language,user.fasteditbtns), reply_markup=keyboards.get_main_keyboard(user.language))
    elif message.text == settingskb.auto_disable_task("rus") or message.text == settingskb.auto_disable_task("eng") :
        user.notifyonce = not user.notifyonce 
        CT.write_json_users(USERlist)
        bot.send_message(chat_id=message.chat.id, text=msg_sets.once_notify_txt(user.language, user.notifyonce), reply_markup=keyboards.get_main_keyboard(user.language))
    elif message.text == settingskb.language_set("rus") or message.text == settingskb.language_set("eng"):
        bot.send_message(chat_id=message.chat.id, text="Please select the language", reply_markup=keyboards.get_language_keyboard())
    elif message.text == settingskb.hide_hints("rus") or message.text == settingskb.hide_hints("eng"):
        user.hidehint = not user.hidehint
        CT.write_json_users(USERlist)
        bot.send_message(chat_id=message.chat.id, text=msg_sets.hide_hints(user.language, user.hidehint) ,reply_markup=keyboards.get_main_keyboard(user.language))
    elif message.text == settingskb.autorofl("rus") or message.text == settingskb.autorofl("eng"):
        user.autorofl = not user.autorofl
        bot.send_message(chat_id=message.chat.id, text=f"{msg_sets.autorofl(user.language, user.autorofl)}", reply_markup=keyboards.get_main_keyboard(user.language))
    elif message.text == "🇷🇺 Russian":
        retUser(message).language = "rus"
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.info_start("rus"), reply_markup=keyboards.get_main_keyboard("rus"))
        CT.write_json_users(USERlist)
    elif message.text == "🇬🇧 English":
        retUser(message).language = "eng"
        bot.send_message(chat_id=message.chat.id, text=msg_tasks.info_start("eng"), reply_markup=keyboards.get_main_keyboard("eng"))
        CT.write_json_users(USERlist)


    
        
@bot.message_handler(commands=['help'])
def help(message):
    echo = bot.send_message(chat_id=message.chat.id,
                            text=msg_tasks.commands_list(retUser(message).language))
    


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
                            bot.send_message(chat_id=user.user_id, text= msg_tasks.loop_error_pair(user.language))
                            continue
                        taskprice = task.price if task.price>0.0001 else "{:^10.8f}".format(task.price)
                        if task.rofl== True and getprice > task.price:
                            kbfastedititems.append(task)
                            task.enable = task.enable if user.notifyonce == False else False
                            printer += msg_tasks.task_printer_raise(user.language,task,getprice)
                        elif task.rofl == False and getprice < taskprice:
                            kbfastedititems.append(task)
                            task.enable = task.enable if user.notifyonce == False else False
                            printer += msg_tasks.task_printer_fall(user.language,task,getprice)
                        elif task.rofl == None:
                            bot.send_message(chat_id=user.user_id, text=f"Some error ocured with task {task.ToShortId()}. Task deleted")
                            TasksList.remove(task)
                            CT.write_json_tasks(TasksList)
                        else:
                            pass
                    if printer == "":
                        time.sleep(1.5)
                    elif printer!= "":
                        rekb = keyboards.get_fast_edit_kb(user.language,kbfastedititems) if user.fasteditbtns else None
                        bot.send_message(chat_id=user.user_id, text=msg_tasks.print_loop(user.language,printer, user.hidehint),reply_markup=rekb)
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