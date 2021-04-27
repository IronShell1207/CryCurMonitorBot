import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import threading
import json
import urllib.request
import requests
import time
import config
import sys
import CryptoTask
import main


def createnewtask_2step(message):
    global main.NewCryptoTask
    NewCryptoTask.base = message.text
    echo = bot.send_message(chat_id=message.chat.id, text=f"Your base currency set as: {NewCryptoTask.base}. Now please send the quote currency (for example: 'USDT')")
    bot.register_next_step_handler(message=echo, callback=createnewtask_3step)

def createnewtask_3step(message):
     global main.NewCryptoTask
    NewCryptoTask.quote = message.text
    echo = bot.send_message(chat_id=message.chat.id, text=f"You have setted the pair: {NewCryptoTask.base}/{NewCryptoTask.quote}. Now send me the price witch you want to get (for example: '0.33')")
    bot.register_next_step_handler(message=echo,callback=createnewtask_4step )

def get_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Raise", callback_data = "CreateRaise"), InlineKeyboardButton("Fall", callback_data = 0))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global main.NewCryptoTask
    if call.data == "1":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "0":
        bot.answer_callback_query(call.id, "Answer is No")

def createnewtask_4step(message):
     global main.NewCryptoTask
    NewCryptoTask.price = float(message.text)
    echo = bot.send_message(chat_id=messaga.chat.id, text=f"Should the price rise to this value or fall? ")

