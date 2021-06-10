import re
import CryptoTask as CT


def created_task_without_rofl(lang, base, quote, price):
    if lang == "rus":
        return f"🔰Пара {base}/{quote} с ценой {price} создана.\nТеперь нужно указать направление движения цены: падение или рост"
    elif lang == "eng":
        return f"🔰Pair {base}/{quote} with value {price} created.\nSelect the movement of value of your pair falling or raising"

def created_task_without_price(lang, base, quote):
    if lang == "rus":
        return f"🔰Пара {base}/{quote} создана.\nТеперь нужно указать ожидаемую цену этой валюты.\nОтправь любое число"
    return f"🔰Pair {base}/{quote} created.\nSpecify the value you want to get for this pair.\nSend any float value"

def created_task_fully(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"✅ Задание мониторинга курса добавлено!\nДетали созданного задания:\n\n{ctask.ToString(lang)}"
    elif lang == "eng":
        return f"✅ Currency exchange rates monitoring task has been created.\nDetails of your task:\n\n{ctask.ToString(lang)}"

def created_task_error_pair(lang):
    if lang == "rus":
        return "❌Крипто пара не найдена. Возможно неверно указана или не существует"
    elif lang == "eng":
        return "❌You have submitted the wrong currency names!"

def created_task_command_only(lang):
    if lang == "rus":
        return "📃 Для создания нового крипто задания отправь мне торговую пару для отслеживания курса (например с биржи binance).\nСначала отправь базовую валюту, например 'BTC', 'LTC', 'ETH'\n\nИли можно отправить полную команду для быстрого создания задания.\nФормат команды:\n/create <базовая валюта> <разменная валюта> <цена> <+ или - для роста или падения цены соответственно>"
    elif lang == "eng":
        return "📃 To create new monitoring task send me the pair witch you want to monitor.\nFirst send me base currency.\n\nExample: 'BTC' 'LTC' 'ETH' (without quotes)\n\nElse you can send full command like:\n/create <base currency name> <quote> <price> <+ or - for raising price or falling>"

def creation_quote_setted(lang: str = "eng", task: CT.CryptoTask = CT.CryptoTask):
    if lang == "rus":
        return f"📝 Создание задания\n\n▶️Ваша пара: {task.base}/{task.quote}.\nТеперь отправь цену, по достижению которой будет отправляться уведомление (например '0.05','1200','0.00000312' без кавычек)"
    return f"📝 Task creation\n\n▶️Your pair: {task.base}/{task.quote}.\nNow tell me the price to be reached\n(for example: '0.05', '1200', '0.000002' without quotes)\nWhen this price is reached, an alert will be sent"

def creation_base_setted(lang, base):
    if lang == "rus":
        return f"📝Создание задания.\n\nВыбранная валюта: {base}.\nТеперь выбери разменную валюту для создания пары."
    elif lang == "eng":
        return f"📝Task creation\n\nYour base currency: {base}. \nNow select quote currency for create pair."

def creation_base_error(lang):
    if lang == "rus":
        return "🚫 Ошибка. Такой валюты не существует"
    elif lang == "eng":
        return "🚫 Error. You have sent wrong currency name"

def creation_price_setted(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"🔰Пара: {ctask.base}/{ctask.quote}.\nЦена:{ctask.price}\nКурс должен 📈 вырасти до такой цены или упасть 📉? Выбери:"
    elif lang == "eng":
        return f"🔰Pair: {ctask.base}/{ctask.quote}.\nPrice:{ctask.price}\nThe course must 📈 rise to such a price or fall 📉?"

def creation_price_error(lang):
    if lang == "rus":
        return f"❌ Цена неверно указана! Создание задания прервано! Придется начать сначала"
    elif lang == "eng":
        return f"❌ You have sent wrong value! Task creation aborted! Send /createtask again."

def creation_final_already_have(lang, ctask: CT.CryptoTask, olctask: CT.CryptoTask):
    if lang == "rus":
        return f"❗️Похожая задача для такой пары уже существует: {ctask.base}/{ctask.quote}.\n{olctask.ToString(lang)}\n\Нужно отредактировать или удалить ее!"
    elif lang == "eng":
        return f"❗️You already have same task: {ctask.base}/{ctask.quote}.\n{olctask.ToString(lang)}\n\You must edit or delete it!"

def creation_selected(lang):
    if lang == "rus":
        return "🔰Выбрано: "
    elif lang == "eng":
        return "🔰You have selected: "

def edited_task_info(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"🖍 Задание отредактировано! Детали:\n\n{ctask.ToString(lang)}"
    elif lang == "eng":
        return f"Task edited! Info:\n\n{ctask.ToString(lang)}"

def editting_task(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"🖍 Редактирование задания:\n{ctask.ToShortStr()}\nДля редактирования задания пришли новую цену или выбери коэфицент изменения цены для быстрого редактирования./nТакже можно отправть полную команду для быстрого редактирования\n/edit <id> <новая цена>"
    elif lang == "eng":
        return f"🖍 You are editting pair:\n{ctask.ToShortStr()}.\nFor edit price send the new one or just select price changing factor.\n\nElse you can send /edit <id> <new_price> to fast edit!"

def editting_task_error(lang):
    if lang == "rus":
        return "🚫 Не указан ID.\nДля редактирования задания отправь команду вида:\n\edit <id задания> <новая цена>* - цена опциональна"
    elif lang == "eng":
        return "🚫 Missing task ID.\nThe command should look like this: \n/edit <task_id> <new_price>* \n* - price is optional"

def id_error(lang):
    if lang == "rus":
        return "🚫Указан неверный ID задания"
    elif lang == "eng":
        return "🚫You have sent wrong task id!"

def pair_monitoring_enabled(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"✅ Мониторинг {ctask.ToShortId()} активирован!"
    elif lang == "eng":
        return f"✅ Pair {ctask.ToShortId()} is now monitoring!"

def pair_monitoring_disabled(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"❗️ Мониторинг {ctask.ToShortId()} деактивирован"
    elif lang == "eng":
        return f"❗️Monitoring disabled for {ctask.ToShortId()}"

def pair_removed(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"❌ Пара {ctask.ToShortId()} удалена!"
    elif lang == "eng":
        return f"❌ Pair ID {ctask.ToShortId()} removed!"

def check_price(lang):
    if lang == "rus":
        return "🔰Для вывода текущего курса обмена валюты пришли мне пару вида: BTC/USDT где <базовая валюта>/<обменная>"
    elif lang == "eng":
        return "🔰To check current exchange rates send me currency pair.\n\nFor example: BTC/USDT or RVN/BTC.\nPlease observe this pattern"

def show_by_task_name(lang):
    if lang == "rus":
        return "❗️Вот список заданий с базовой валютой - "
    elif lang == "eng":
        return "❗️Your list with base - "

def show_by_task_name_err(lang):
    if lang == "rus":
        return "❌У вас нет заданий с такой базовой валютой - "
    elif lang == "eng":
        return "❌You have no any tasks with such base currency - "

def current_price_pair(lang):
    if lang == "rus":
        return "💸Текущий курс обмена пары "
    elif lang == "eng":
        return "💸Current price for pair "

def wrong_pair(lang, base, quote):
    if lang == "rus":
        return f"🚫 Пара {base}/{quote} не найдена!"
    elif lang == "eng":
        return f"🚫I can't find pair {base}/{quote}!"

def stop_all_tasks(lang):
    if lang == "rus":
        return "⛔️ Все задания остановлены"
    elif lang == "eng":
        return "⛔️ All tasks are stopped."

def no_tasks_detected(lang):
    if lang == "rus":
        return "❌ У вас нет ниодного задания для мониторинга!"
    elif lang == "eng":
        return "❌ You have not added any tasks yet!"

def start_all_tasks(lang, ix, alon):
    if lang == "rus":
        alreadyon = f"and {alon-ix} были активированы ранее ✅" if alon-ix>0 else ""
        return f"✅Ваши {ix} заданий активированы, и {alreadyon} "
    elif lang == "eng":
        alreadyon = f"and {alon-ix} tasks already ON ✅" if alon-ix>0 else ""
        
        return f"✅Your {ix} monitoring tasks are started and {alreadyon} started"

def editted_task_info(lang):
    if lang == "rus":
        return "🖍 Задание отредактировано! Инфа:\n\n"
    elif lang == "eng":
        return "🖍 Task edited! Info:\n\n"

def wrong_value_error(lang):
    if lang == "rus":
        return "❌ Вы отправили неправильное значение!"
    elif lang == "eng":
        return '❌ You have sent wrong value!'

def all_tasks_removed(lang):
    if lang == "rus":
        return "❌Все задания мониторинга удалены!❌"
    elif lang == "eng":
        return f"❌Your monitoring list has been fully removed❌"

def action_outdated(lang):
    if lang == "rus":
        return "🚫 Действие устарело!"
    elif lang == "eng":
        return "🚫 Action is outdated."

def trigger_moved(lang, old_pr, pr, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"\n\n☑️ Триггер уведомления передвинут с {old_pr} на {pr} для {ctask.ToShortId()}"
    elif lang == "eng":
        return f"\n\n☑️ Trigger moved from {old_pr} to {pr} for {ctask.ToShortId()}"

def task_edit_request(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"🖍 Редактирование {ctask.ToShortStr()}.\nВыбери коэфициент изменения цены или укажи новую"
    elif lang == "eng":
        return f"🖍 You are editting pair: {ctask.ToShortStr()}.\nSelect price changing factor or you can set your value."

def task_new_override(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"🖍Задание переписано!\nДетали задания:\n{ctask.ToString(lang)}"
    elif lang == "eng":
        return f"Your task overrided. \nDetails of your task:\n{ctask.ToString(lang)}"

def new_value_set(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"🖍Для установки новой цены для пары {ctask.ToShortStr()} отправь цену в следующем сообщении!"
    elif lang == "eng":
        return f"🖍To set a new value for pair {ctask.ToShortStr()} send it in next message"

def clear_tasks_list_request(lang):
    if lang == "rus":
        return "❌ Вы уверены что хотите очистить список заданий?\nДействие отменить нельзя!"
    elif lang == "eng":
        return "❌ Are you sure you want to clear the tracking list?\nAction cannot be undone"

def return_rates_tasks(lang):
    if lang == "rus":
        return f"📈📉Ваш список курсов пар, добавленных ранее:\n\n"
    elif lang == "eng":
        return f"📈📉Your currency exchange rates, based on your tasks: \n\n"

def return_monitoring_list(lang, printer, hints):
    if lang == "rus":
        if not hints:
            return f"Ваш список заданий:\n\n{printer}\nЧтобы получить отфильтрованный по базовой валюте список заданий пришли команду следующего вида:\n/show <название валюты>"
        else:
            return f"Ваш список заданий:\n\n{printer}"
    elif lang == "eng":
        if not hints:
            return f"Your monitoring task list:\n\n{printer}\nTo get filtred list by base send: /show <base currency>"
        else:
            return f"Your monitoring task list:\n\n{printer}"

def info_start(lang):
    if lang == "rus":
        return "Привет! Я бот для мониторинга курсов криптовалют. Добавь задания и я отправлю тебе уведомление о увеличении📉 или уменьшении цены📈 до того значения, которое ты выставишь💰.\n📋Список доступных команд ты можешь получить командой: /help\nИнформацию о данном боте🔎: /info"
    elif lang == "eng":
        return "Hello! I'm crypto currency exchange monitor bot. I can send you 💬 notification when your currency is raise 📉 or fall 📈 to setted value 💰. \nFor create new task 🖍 send: /createtask.\nFor get info 📋 send: /info\nFor get all available commands 🔎 send: /help"

def info_bot(lang):
    if lang == "rus":
        return """Краткая информация о данном боте:
Данный бот разработан на python3 и работает на библиотеке pyTelegramBotAPI.
Бот присылает уведомления о изменениях курсов валют, которые ты добавишь. 
Бот запрашивает курсы напрямую с API Binancе, так что данные актуальны на текущее время.
🛸 Код данного бота доступен на Github: https://github.com/IronShell1207/CryCurMonitorBot
⛏ Разработал: Ironshell
Мой сайт: https://droidapps.cf/ разный софт, а также полезные гайды
Если тебе захочется поддержать меня, мои кошельки 
\n🥇ETH: 0xa35fbab442da4e65413045a4b9b147e2a0fc3e0c\n🎈LTC: LQiBdMeCNWAcSBEhc2QT3ffFz8a2t7zPcG"""
    elif lang == "eng":
        return """Brief information about this bot: 
This bot is written on Python3 with pyTelegramBotApi library.
This bot uses realtime binance exchange rates!
⛏ Developer: Ironshell
🛸 Github: https://github.com/IronShell1207/CryCurMonitorBot
My web: https://droidapps.cf/en/
If bot is usefull for you, you can buy my a ☕️ and thx 2u).
\n🥇ETH: 0xa35fbab442da4e65413045a4b9b147e2a0fc3e0c\n🎈LTC: LQiBdMeCNWAcSBEhc2QT3ffFz8a2t7zPcG
"""

def commands_list(lang):
    if lang == "rus":
        return """Список команд:
1. Для создания заданий используется команда - /create
или для быстрого создания  
/create <база> <размен> <Цена> <+ или - для роста или падения цены>
2. Запуск всех заданий - /turnontasks
3. Остановка всех заданий - /stopalltasks
4. Показать все созданные задания - /showtasks
5. Отключить задание по ID - /disable <id>
6. Запуск задания по ID - /enable <id>
7. Редактировать задание /edit <id>
или для быстрого редактирования цены
/edit <id> <новая цена>
8. Удалить задание - /remove <id>
9. Задать задержку между уведомлениями - /settimer <sec>
10. Вывести курсы обмена всех заданий - /getrates
11. Показать задания по названию валюты (например BTC)
/show <base>

*Треугольные скобки указывать не нужно!
 """
    elif lang == "eng":
        return """Commands list:
1. Create new monitoring task - /createtask
or /createtask <base> <quote> <price> <+|-> ("+" for choose raising or "-" for falling price)
2. Start all monitoring tasks - /turnontasks
3. Stop all monitoring tasks - /stopalltasks
4. Show all tasks /showtasks
5. Disable monitoring by ID - /disable <id>
6. Start monitoring by ID - /enable <id>
7. Edit task - /edit <id>
8. Delete task /remove <id>
9. Set notification delay (seconds) - /settimer <secs>
10. Change notification style from separate messages to single - /setstyle
11. Get all current exchange rates - /getrates
12. Show tasks by base currency name - /show <base>

*Send commands without brackets only"""



def task_printer_raise(lang, ctask: CT.CryptoTask, newprice):
    if lang == "rus":
        return f"🔺 {ctask.ToShortId()} цена выросла 📈 c {ctask.price} до {newprice}!\n"
    elif lang == "eng":
        return f"🔺 {ctask.ToShortId()} price raise 📈 from {ctask.price} to {newprice}!\n" 

def task_printer_fall(lang, ctask: CT.CryptoTask, newprice):
    if lang == "rus":
        return f"🔺 {ctask.ToShortId()} цена упала 📉 c {ctask.price} до {newprice}!\n"
    elif lang == "eng":
        return f"🔺 {ctask.ToShortId()} price fall 📉 from {ctask.price} to {newprice}!\n" 

def print_loop(lang, printer, ishints):
    if lang == "rus":
        if not ishints:
            return  f"⚠️ Уведомление о достижении целей по курсам:\n{printer}\nДля редактирования задания отправь:\n/edit <id> <цена>\nДля отключения задания:\n/disable <id>\n*Отключить кнопки быстрого редактирования можно в настройках ⚙️!"
        else:
            return printer
    elif lang == "eng":
        if not ishints:
            return f"⚠️ Your updated exchange rates list:\n{printer}\nTo edit task send: /edittask <task id>\nTo disable: /disable <task_id>*To disable fast edit buttons go to the settings ⚙️!"
        else:
            return printer

def loop_error_pair(lang, ctask: CT.CryptoTask):
    if lang == "rus":
        return f"Что-то пошло не так с запросом курса для пары:{ctask.base}/{ctask.quote}"
    elif lang == "eng":
        return f"Something went wrong with price checking of pair {ctask.base}/{ctask.quote}"