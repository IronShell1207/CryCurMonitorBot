
def notify_timeout(lng):
    if lng == "rus":
        return "🕘Задержка оповещ."
    elif lng == "eng":
        return "🕘Notification timeout"

def auto_enable_not(lng):
    if lng == "rus":
        return "✅Автозапуск новых"
    elif lng == "eng":
        return "✅Auto enable new task"
    
def show_edit_btns(lng):
    if lng == "rus":
        return "📝Вкл. кнопки редактирования"
    elif lng == "eng":
        return "📝Show edit buttons"
    
def auto_disable_task(lng):
    if lng == "rus":
        return "⛔️ Откл. задание после уведм."
    elif lng == "eng":
        return "⛔️ Disable task after trigger"
    
def language_set(lng):
    if lng == "rus":
        return "🇷🇺🇺🇸 Язык"
    elif lng == "eng":
        return "🇷🇺🇺🇸 Language"
    
def back_sets_btn(lng):
    if lng == "rus":
        return "◀️ Назад"
    elif lng == "eng":
        return "◀️ Back"

def hide_hints(lng):
    if lng == "rus":
        return "Скрыть подсказки📃"
    elif lng == "eng":
        return "Hide hints 📃"


def bottom_kb_settings(lng: str = "eng"):
    return [notify_timeout(lng),auto_enable_not(lng),
            show_edit_btns(lng),auto_disable_task(lng),
            language_set(lng),hide_hints(lng),
            back_sets_btn(lng),"🇬🇧 English", "🇷🇺 Russian"]


