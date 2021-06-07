
def mg_dont_accept_err(lang):
    if lang == "rus":
        return "⛔️ Что ты мне такое тут прислал???"
    return "⛔️ I dont accept this. I will send it to my admin!!"
def lal(lang):
    if lang == "rus":
        return "Ты чего тут забыл говорю?"
    return "What are you looking for round there?"

def autoenable_message(lang):
    if lang == "rus":
        return "Авто активация новых заданий вкл.: {0}"
    return "Auto enabling new tasks active status: {0}"

def notification_delay_set(lang):
    if lang == "rus":
        return 'Отправь мне количество секунд для установки задержки между оповещениями по обновлению цен.'
    return "Send me number of seconds for notification delay (this only works for changing the delay between notifications)"