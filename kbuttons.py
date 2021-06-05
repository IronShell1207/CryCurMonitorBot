
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

