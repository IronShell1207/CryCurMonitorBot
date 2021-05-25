from sre_constants import MARK
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import telebot

def get_raise_fall_kb():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Raise 📈", callback_data = "CreateRaise"), InlineKeyboardButton("Fall 📉", callback_data = "CreateFall"))
    return markup


def get_edit_price_keyboard(idtask: int, rofl: bool):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    itemROD = "🔺 by +{0}%" if rofl else "🔻 by -{0}%"
    itemROData = "t/up{0}/"+str(idtask) if rofl else "t/dn{0}/"+str(idtask)
    item1 =InlineKeyboardButton("Disable ⛔️", callback_data = f"t/disable/{idtask}")
    #item2 =InlineKeyboardButton("Edit task ✏️", callback_data = f"t/edittask/{idtask}")
    item3 =InlineKeyboardButton(itemROD.format("5"), callback_data = itemROData.format(5))
    item4 =InlineKeyboardButton(itemROD.format("2"), callback_data = itemROData.format(2))
    item5 =InlineKeyboardButton(itemROD.format("1"), callback_data = itemROData.format(1))
    item6 = InlineKeyboardButton("New value ✏️", callback_data=f"t/newv{str(idtask)}")
    #item3 =InlineKeyboardButton("Remove task ❌", callback_data=f"t/removetask/{idtask}")
    markup.add(item5, item4 ,item3,item1,item6)
    return markup

def get_remove_edit_kb(idtask: int):
    markup = InlineKeyboardMarkup()
    item1 =InlineKeyboardButton("Disable ⛔️", callback_data = f"t/disable/{idtask}")
    item2 =InlineKeyboardButton("Edit task ✏️", callback_data = f"t/edittask/{idtask}")
    markup.add(item1, item2)
    return markup

def get_startup_keys():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton("Create new task 📊", callback_data="createtask")
    item2 = InlineKeyboardButton("View my tasks 📝",callback_data="viewtasks")
    markup.add(item1, item2)
    return markup

def get_create_only():
    markup = InlineKeyboardMarkup([InlineKeyboardButton("Create task 📊",callback_data="createtask")]) 
    return markup

def get_starttask_keys(idtask: int):
    markup = InlineKeyboardMarkup()
    markup.row_width=2
    item1 = InlineKeyboardButton("Start task ✅", callback_data=f"t/starttask/{idtask}")
    item2 = InlineKeyboardButton("New task 📊", callback_data=f"createtask")
    item3 = InlineKeyboardButton("View my tasks 📝",callback_data="viewtasks")
    markup.add(item1, item2, item3)
    return markup

def get_en_dis_all_keys():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton("Start all ▶️", callback_data="turnontasks")
    item2 = InlineKeyboardButton("Disable all ⏸", callback_data="stopalltasks")
    item3 = InlineKeyboardButton("❗️Remove all❕", callback_data="removealltasks")
    markup.add(item1, item2, item3)
    return markup


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    
    item1 = KeyboardButton("Display tasks list 📝")
    item2 = KeyboardButton("Create new 📊")
    item5 = KeyboardButton("Settings ⚙️")
    item3 = KeyboardButton("Start all ▶️")
    item4 = KeyboardButton("Disable all ⏸")
    item6 = KeyboardButton("Display rates ✅")
    markup.add(item1, item2,item5, item3, item4, item6)
    return markup

def get_settings_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    
    item1 = KeyboardButton("🕘Notification timeout")
    item2 = KeyboardButton("✅Auto enable new task")
    markup.add(item1,item2)
    return markup

def get_quotes_keyboard(listitems: list):
    markup = InlineKeyboardMarkup()  
    for item in listitems:
        ikey = InlineKeyboardButton(item,callback_data=f"n/{item}")
        markup.add(ikey)
    return markup