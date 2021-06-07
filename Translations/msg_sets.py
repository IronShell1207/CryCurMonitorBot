def autoenable_message(lang):
    if lang == "rus":
        return "Авто активация новых заданий вкл.: {0}"
    return "Auto enabling new tasks active status: {0}"

def notification_delay_set(lang):
    if lang == "rus":
        return 'Отправь мне количество секунд для установки задержки между оповещениями по обновлению цен.'
    return "Send me number of seconds for notification delay (this only works for changing the delay between notifications)"

def close_setting_menu(lang):
    if lang == "rus":
        return 'Настройки закрыты!'
    return 'Settings have been closed!'

def fastEditBtns_txt(lang, hord):
    if lang == "rus":
        hjd = 'отображаются! ✅' if hord else "скрыты! ❌"
        return f"⚠️ Кнопки быстрого редактирования теперь {hjd}"
    hjd = "displaying! ✅" if hord else "hidden! ❌"
    return f"⚠️ Fast edit buttons now {hjd}"

def once_notify_txt(lang, eod):
    if lang == "rus":
        ans = "каждый раз" if eod else "один раз"
        return f"Уведомления о изменениях теперь срабатывают {ans}"
    ans = "every time" if eod else "once"
    return f"Now task notifications will be triggered {ans}"