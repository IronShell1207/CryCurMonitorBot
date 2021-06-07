def display_tasks(lng):
    if lng == "rus":
        return "Список заданий 📝"
    return "Display tasks list 📝"

def create_new_task(lng):
    if lng == "rus":
        return "Создать 📊"
    return "Create new 📊"

def settings(lng):
    if lng == "rus":
        return "Установки ⚙️"
    return "Settings ⚙️"

def start_all_tasks_btn(lng):
    if lng == "rus":
        return "Запуск всех ▶️"
    return "Start all ▶️"
def disable_all_tasks_btn(lng):
    if lng == "rus":
        return "Выкл. все задания ⏸"
    return "Disable all ⏸"
def display_rates(lng):
    if lng == "rus":
        return "Тек. цены по заданиям ✅"
    return "Display rates ✅"
    
def get_main_kb_buttons(lng):
    return [display_tasks(lng),create_new_task(lng),
            settings(lng),start_all_tasks_btn(lng),
            disable_all_tasks_btn(lng),display_rates(lng)]