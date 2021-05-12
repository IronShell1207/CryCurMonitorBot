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
import regexcombs as rx


TasksList = []
tasksjsn = CT.get_json_task_list()
if tasksjsn != None:
    TasksList=tasksjsn


sleeptimer = 90
USERlist=[]
def checkifnewuser(message):
    for user in USERlist:
        if user.user_id == message.chat.id:
            return
    mainthread = threading.Thread(target=tasks_loop,args=[message])
    mainthread.start()
    user = CT.UserSets(user_id=message.chat.id, notifytimer = 90)
    USERlist.append(user)