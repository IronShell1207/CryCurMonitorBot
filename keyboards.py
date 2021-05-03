from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot

def get_raise_fall_kb():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Raise 📈", callback_data = "CreateRaise"), InlineKeyboardButton("Fall 📉", callback_data = "CreateFall"))
    return markup


def get_disable_task_kb(idtask: int):
    markup = InlineKeyboardMarkup()
    item1 =InlineKeyboardButton("Disable ⛔️", callback_data = f"t/disable/{idtask}")
    item2 =InlineKeyboardButton("Edit task ✏️", callback_data = f"t/edittask/{idtask}")
    item3 =InlineKeyboardButton("Remove task ❌", callback_data=f"t/removetask/{idtask}")
    markup.add(item1, item2, item3)
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
    markup.max_row_keys= 2
    item1 = InlineKeyboardButton("Start task ✅", callback_data=f"t/starttask/{idtask}")
    item2 = InlineKeyboardButton("New task 📊", callback_data=f"createtask")
    item3 = InlineKeyboardButton("View my tasks 📝",callback_data="viewtasks")
    markup.add(item1, item2, item3)
    return markup

def get_en_dis_all_keys():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton("Start all tasks ▶️", callback_data="startalltasks")
    item2 = InlineKeyboardButton("Disable all tasks ⏸", callback_data="stopalltasks")
    markup.add(item1, item2)
    return markup

