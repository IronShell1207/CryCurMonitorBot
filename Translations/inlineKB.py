
def create_task(lng):
    if lng == "rus":
        return "Новое задание 📊"
    elif lng == "eng":
        return "New task 📊"

def check_tasks(lng):
    if lng == "rus":
        return "Просмотреть задания📝"
    elif lng == "eng":
        return "View my tasks 📝"

def starttask(lng):
    if lng == "rus":
        return "Запуск ✅"
    elif lng == "eng":
        return "Start task ✅"

def disabletask(lng):
    if lng == "rus":
        return "Выкл. ⛔️"
    elif lng == "eng":
        return "Disable ⛔️"

def edit_task(lng):
    if lng == "rus":
        return "Изм. ✏️"
    elif lng == "eng":
        return "Edit task ✏️"

def add_anyway(lng):
    if lng == "rus":
        return "Добавить все равно ✅"
    elif lng == "eng":
        return "Add anyway ✅"

def override(lng):
    if lng == "rus":
        return "Перезаписать ⬆️"
    elif lng == "eng":
        return "Override ⬆️"

def removetask(lng):
    if lng == "rus":
        return "Удалить ❌"
    elif lng == "eng":
        return "Remove task ❌"

def newvalue(lng):
    if lng == "rus":
        return "Вручную ✏️"
    elif lng == "eng":
        return "New value ✏️"

def raise_val(lng):
    if lng == "rus":
        return "Рост 📈"
    elif lng == "eng":
        return "Raise 📈"

def fall(lng):
    if lng == "rus":
        return "Падение 📉"
    elif lng == "eng":
        return "Fall 📉"

def remove_all_yes(lng):
    if lng == "rus":
        return "✅ Да удалить все"
    elif lng == "eng":
        return "✅ YES remove all"
    
def remove_all_no(lng):
    if lng == "rus":
        return "❌ Нет (пощадить)"
    elif lng == "eng":
        return "❌ No (to spare)"

def stop_all(lng):
    if lng == "rus":
        return "Остановить все ⏸"
    elif lng == "eng":
        return "Disable all ⏸"

def remove_all(lng):
    if lng == "rus":
        return "❗️Удалить все❕"
    elif lng == "eng":
        return "❗️Remove all❕"