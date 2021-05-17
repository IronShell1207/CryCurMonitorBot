from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import telebot

def get_raise_fall_kb():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Raise 📈", callback_data = "CreateRaise"), InlineKeyboardButton("Fall 📉", callback_data = "CreateFall"))
    return markup


def get_disable_task_kb(idtask: int, rofl: bool):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    itemROD = "🔺 by +{0}%" if rofl else "🔻 by -{0}%"
    itemROData = "t/up{0}/"+str(idtask) if rofl else "t/dn{0}/"+str(idtask)
    item1 =InlineKeyboardButton("Disable ⛔️", callback_data = f"t/disable/{idtask}")
    item2 =InlineKeyboardButton("Edit task ✏️", callback_data = f"t/edittask/{idtask}")
    item3 =InlineKeyboardButton(itemROD.format("5"), callback_data = itemROData.format(5))
    item4 =InlineKeyboardButton(itemROD.format("2"), callback_data = itemROData.format(2))
    item5 =InlineKeyboardButton(itemROD.format("1"), callback_data = itemROData.format(1))
    #item3 =InlineKeyboardButton("Remove task ❌", callback_data=f"t/removetask/{idtask}")
    markup.add(item5, item4 ,item3,item1, item2,)
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
    item1 = InlineKeyboardButton("Start all tasks ▶️", callback_data="turnontasks")
    item2 = InlineKeyboardButton("Disable all tasks ⏸", callback_data="stopalltasks")
    markup.add(item1, item2)
    return markup


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    
    item1 = KeyboardButton("View my tasks 📝")
    item2 = KeyboardButton("Create new task 📊")
    item5 = KeyboardButton("Check price 💸")
    item3 = KeyboardButton("Start all tasks ▶️")
    item4 = KeyboardButton("Disable all tasks ⏸")
    item6 = KeyboardButton("All exchange rates ✅")
    markup.add(item1, item2,item5, item3, item4, item6)
    return markup

def get_quotes_keyboard(listitems: list):
    markup = InlineKeyboardMarkup()
    for item in listitems:
        ikey = InlineKeyboardButton(item,callback_data=f"n/{item}")
        markup.add(ikey)
    return markup
