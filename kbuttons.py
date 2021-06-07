
def notify_timeout(lng):
    if lng == "eng":
        return "🕘Notification timeout"
    elif lng == "rus":
        return "🕘Задержка оповещ."

def auto_enable_not(lng):
    if lng == "eng":
        return "✅Auto enable new task"
    elif lng == "rus":
        return "✅Автозапуск новых"
    
def show_edit_btns(lng):
    if lng == "eng":
        return "📝Show edit buttons"
    elif lng == "rus":
        return "📝Вкл. кнопки редактирования"
    
def auto_disable_task(lng):
    if lng == "eng":
        return "⛔️ Disable task after trigger"
    elif lng == "rus":
        return "⛔️ Откл. задание после уведм."
    
def language_set(lng):
    if lng == "eng":
        return "🇷🇺🇺🇸 Language"
    elif lng == "rus":
        return "🇷🇺🇺🇸 Язык"
    
def back_sets_btn(lng):
    if lng == "eng":
        return "◀️ Back"
    elif lng == "rus":
        return "◀️ Назад"

def bottom_kb_settings(lng):
    return [notify_timeout(lng),auto_enable_not(lng),
            show_edit_btns(lng),auto_disable_task(lng),
            language_set(lng),back_sets_btn(lng)]



def display_tasks(lng):
    if lng == "eng":
        return "Display tasks list 📝"
    elif lng == "rus":
        return "Список заданий 📝"

def create_new_task(lng):
    if lng == "eng":
        return "Create new 📊"
    elif lng == "rus":
        return "Создать 📊"

def settings(lng):
    if lng == "eng":
        return "Settings ⚙️"
    elif lng == "rus":
        return "Установки ⚙️"

def start_all_tasks_btn(lng):
    if lng == "eng":
        return "Start all ▶️"
    elif lng == "rus":
        return "Запуск всех ▶️"
def disable_all_tasks_btn(lng):
    if lng == "eng":
        return "Disable all ⏸"
    elif lng == "rus":
        return "Выкл. все задания ⏸"
def display_rates(lng):
    if lng == "eng":
        return "Display rates ✅"
    elif lng == "rus":
        return "Тек. цены по заданиям ✅"
    
def get_main_kb_buttons(lng):
    return [display_tasks(lng),create_new_task(lng),
            settings(lng),start_all_tasks_btn(lng),
            disable_all_tasks_btn(lng),display_rates(lng)]