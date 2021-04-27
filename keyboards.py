from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot

def get_raise_fall_kb():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Raise 📈", callback_data = "CreateRaise"), InlineKeyboardButton("Fall 📉", callback_data = "CreateFall"))
    return markup