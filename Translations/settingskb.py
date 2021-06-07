
def notify_timeout(lng):
    if lng == "rus":
        return "🕘Задержка оповещ."
    return "🕘Notification timeout"

def auto_enable_not(lng):
    if lng == "rus":
        return "✅Автозапуск новых"
    return "✅Auto enable new task"
    
def show_edit_btns(lng):
    if lng == "rus":
        return "📝Вкл. кнопки редактирования"
    return "📝Show edit buttons"
    
def auto_disable_task(lng):
    if lng == "rus":
        return "⛔️ Откл. задание после уведм."
    return "⛔️ Disable task after trigger"
    
def language_set(lng):
    if lng == "rus":
        return "🇷🇺🇺🇸 Язык"
    return "🇷🇺🇺🇸 Language"
    
def back_sets_btn(lng):
    if lng == "rus":
        return "◀️ Назад"
    return "◀️ Back"

def bottom_kb_settings(lng):
    return [notify_timeout(lng),auto_enable_not(lng),
            show_edit_btns(lng),auto_disable_task(lng),
            language_set(lng),back_sets_btn(lng),"🇬🇧 English", "🇷🇺 Russian"]



