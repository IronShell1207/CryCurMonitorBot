from sre_constants import MARK
from subprocess import call
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import telebot

from Translations import settingskb, mainkb, inlineKB

def get_raise_fall_kb(lng):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    item1 = InlineKeyboardButton(inlineKB.raise_val(lng),callback_data = "CreateRaise")
    item2 = InlineKeyboardButton(inlineKB.fall(lng), callback_data = "CreateFall")
    markup.add(item1, item2 )
    return markup


def get_edit_price_keyboard(lng,idtask: int, rofl: bool, enable: bool):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    itemROD = "🔺 by +{0}%" if rofl else "🔻 by -{0}%"
    itemROData = "t/up{0}/"+str(idtask) if rofl else "t/dn{0}/"+str(idtask)
    item1 = InlineKeyboardButton(inlineKB.disabletask(lng), callback_data = f"t/disable/{idtask}") if enable == True else InlineKeyboardButton("Start ✅", callback_data = f"t/starttask/{idtask}")
    #item2 =InlineKeyboardButton("Edit task ✏️", callback_data = f"t/edittask/{idtask}")
    item3 = InlineKeyboardButton(itemROD.format("5"), callback_data = itemROData.format(5))
    item4 = InlineKeyboardButton(itemROD.format("2"), callback_data = itemROData.format(2))
    item5 = InlineKeyboardButton(itemROD.format("1"), callback_data = itemROData.format(1))
    item6 = InlineKeyboardButton(inlineKB.newvalue(lng), callback_data=f"t/newv/{str(idtask)}")
    item7 =InlineKeyboardButton(inlineKB.removetask(lng), callback_data=f"t/removetask/{idtask}")
    markup.add(item5, item4 ,item3,item1,item6, item7)
    return markup

def get_remove_edit_kb(lng, idtask: int):
    markup = InlineKeyboardMarkup()
    markup.row_width=2
    item1 =InlineKeyboardButton(inlineKB.disabletask(lng), callback_data = f"t/disable/{idtask}")
    item2 =InlineKeyboardButton(inlineKB.edit_task(lng), callback_data = f"t/edittask/{idtask}")
    item3 = InlineKeyboardButton(inlineKB.add_anyway(lng), callback_data=f"createanyway")
    item4 = InlineKeyboardButton(inlineKB.override(lng), callback_data=f"t/overridetask/{idtask}")
    markup.add(item1, item2, item3, item4)
    return markup

def get_startup_keys(lng):
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton(inlineKB.create_task(lng), callback_data="createtask")
    item2 = InlineKeyboardButton(inlineKB.check_tasks(lng),callback_data="viewtasks")
    markup.add(item1, item2)
    return markup

def get_create_only(lng):
    markup = InlineKeyboardMarkup() 
    item = InlineKeyboardButton(inlineKB.create_task(lng),callback_data="createtask")
    markup.add(item)
    return markup

def get_remove_cfrm(lng):
    markup = InlineKeyboardMarkup(row_width=1)
    item1 = InlineKeyboardButton(inlineKB.remove_all_yes(lng), callback_data="removealltasks")
    item2 = InlineKeyboardButton(inlineKB.remove_all_no(lng), callback_data="none")
    markup.add(item1, item2)
    return markup

def get_starttask_keys(lng, idtask: int):
    markup = InlineKeyboardMarkup()
    markup.row_width=2
    item1 = InlineKeyboardButton(inlineKB.starttask(lng), callback_data=f"t/starttask/{idtask}")
    item2 = InlineKeyboardButton(inlineKB.create_task(lng), callback_data=f"createtask")
    item3 = InlineKeyboardButton(inlineKB.check_tasks(lng),callback_data="viewtasks")
    markup.add(item1, item2, item3)
    return markup

def get_en_dis_all_keys(lng):
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton(mainkb.start_all_tasks_btn(lng), callback_data="turnontasks")
    item2 = InlineKeyboardButton(inlineKB.stop_all(lng), callback_data="stopalltasks")
    item3 = InlineKeyboardButton(inlineKB.remove_all(lng), callback_data="removetasksqu")
    markup.add(item1, item2, item3)
    return markup

def get_language_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = KeyboardButton("🇬🇧 English")
    item2 = KeyboardButton("🇷🇺 Russian")
    markup.add(item1,item2)
    return markup

def get_main_keyboard(lng):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    item1 = KeyboardButton(mainkb.display_tasks(lng))
    item2 = KeyboardButton(mainkb.create_new_task(lng))
    item5 = KeyboardButton(mainkb.settings(lng))
    item3 = KeyboardButton(mainkb.start_all_tasks_btn(lng))
    item4 = KeyboardButton(mainkb.disable_all_tasks_btn(lng))
    item6 = KeyboardButton(mainkb.display_rates(lng))
    markup.add(item1, item2,item5, item3, item4, item6)
    return markup

def get_settings_kb(lng):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    item1 = KeyboardButton(settingskb.notify_timeout(lng))
    item2 = KeyboardButton(settingskb.auto_enable_not(lng))
    item6 = KeyboardButton(settingskb.show_edit_btns(lng))
    item4 = KeyboardButton(settingskb.auto_disable_task(lng))
    item5 = KeyboardButton(settingskb.language_set(lng))
    item3 = KeyboardButton(settingskb.back_sets_btn(lng))
    item7 = KeyboardButton(settingskb.autorofl(lng))
    itemhints = KeyboardButton(settingskb.hide_hints(lng))
    itemantiflood = KeyboardButton(settingskb.antiflood(lng))
    
    markup.add(item1,item2,item6,item4,item5,itemhints,item7,item3)
    return markup

def get_quotes_keyboard(listitems: list):
    markup = InlineKeyboardMarkup()  
    for item in listitems:
        ikey = InlineKeyboardButton(item,callback_data=f"n/{item}")
        markup.add(ikey)
    return markup


def get_fast_edit_kb(lng, listitems: list):
    markup =InlineKeyboardMarkup()
    for item in listitems:
        ikey = InlineKeyboardButton(f"{inlineKB.edit_task(lng)} {item.ToShortStr()} ", callback_data=f"t/edittask/{item.id}")
        markup.add(ikey)
    return markup