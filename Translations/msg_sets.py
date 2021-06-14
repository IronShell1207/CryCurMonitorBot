import CryptoTask as CT

def autoenable_message(lang):
    if lang == "rus":
        return "Авто активация новых заданий вкл.: {0}"
    elif lang == "eng":
        return "Auto enabling new tasks active status: {0}"

def notification_delay_set(lang):
    if lang == "rus":
        return 'Отправь мне количество секунд для установки задержки между оповещениями по обновлению цен.'
    elif lang == "eng":
        return "Send me number of seconds for notification delay (this only works for changing the delay between notifications)"

def close_setting_menu(lang):
    if lang == "rus":
        return 'Настройки закрыты!'
    elif lang == "eng":
        return 'Settings have been closed!'

def fastEditBtns_txt(lang, hord):
    if lang == "rus":
        hjd = 'отображаются! ✅' if hord else "скрыты! ❌"
        return f"⚠️ Кнопки быстрого редактирования теперь {hjd}"
    elif lang == "eng":
        hjd = "displaying! ✅" if hord else "hidden! ❌"
        return f"⚠️ Fast edit buttons now {hjd}"

def once_notify_txt(lang, eod):
    if lang == "rus":
        ans = "один раз" if eod else "каждый раз"
        return f"Уведомления о изменениях теперь срабатывают {ans}"
    elif lang == "eng":
        ans = "once" if eod else "every time"
        return f"Now task notifications will be triggered {ans}"

def notify_timer(lang, sec: float = 0):
    if lang == "rus":
        return f"📣Задержка между уведомлениями об изменениях курсов установлено на {sec}сек.🕒"
    elif lang == "eng":
        return f"📣Notification delay setted on {sec}sec.🕒"

def wrong_value(lang):
    if lang == "rus":
        return "❌Неправильно указано значение!"
    elif lang == "eng":
        return "❌Wrong value!"

def current_sets(user : CT.UserSets):
    if user.language == "rus":
        return f"""🛠Текущие настройки пользователя {user.user_id}:
- Язык: {user.language}
- Автозапуск новых заданий: {user.autostartcreate}
- Кнопки быстрого редактирования заданий при уведомлении о изменении курсов: {user.fasteditbtns}
- Авто отключение задания после одного уведомления (уведомления приходят всегда после достижении целей при выключенной функции): {user.notifyonce}
- Задержка между уведомлениями: {user.notifytimer}
- Скрытие подсказок: {user.hidehint}
- Автоматическое определение движение цены при создании задания {user.autorofl}

Редактирование настроек производится с помощью клавиатуры ниже"""
    elif user.language == "eng":
        return f"""🛠Current settings of user {user.user_id}:
- Language: {user.language}
- Auto starting new tasks: {user.autostartcreate}
- Displaying task fast edit buttons after notify: {user.fasteditbtns}
- Auto disabling tasks after single trigger (trigger always after cource reaches setted price if disabled): {user.notifyonce} 
- Delay between notifications: {user.notifytimer}
- Hidding hints: {user.hidehint}
- Automatic determination of the direction of price movement {user.autorofl}

You can edit settings by the keyboard bellow"""


def hide_hints(lng, ishide):
    if lng == "rus":
        sll ="скрыты" if ishide else "отображаются"
        return f"📃Подсказки в сообщениях теперь {sll}"
    elif lng == "eng":
        sll = "hidded" if ishide else "displayed"
        return f"📃Hints are now {sll}!"
    
def autorofl(lng,rofl):
    if lng == "rus":
        return f"Авто определение роста или падения цены в зависимости от установленной цели при создании задачи: {'активировано ✅' if rofl else 'отключено ❌'}"
    elif lng == "eng":
        return f"Automatic detection of the rise or fall of the price depending on the set goal when creating a task: {'enabled ✅' if rofl else 'disabled ❌'}"