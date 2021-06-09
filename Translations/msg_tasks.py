import re


def created_task_without_rofl(lang, base, quote, price):
    if lang == "rus":
        return f"🔰Пара {base}/{quote} с ценой {price} создана.\nТеперь нужно указать направление движения цены: падение или рост"
    return f"🔰Pair {base}/{quote} with value {price} created.\nSelect the movement of value of your pair falling or raising"

def created_task_without_price(lang, base, quote):
    if lang == "rus":
        return f"🔰Пара {base}/{quote} создана.\nТеперь нужно указать ожидаемую цену этой валюты.\nОтправь любое число"
    return f"🔰Pair {base}/{quote} created.\nSpecify the value you want to get for this pair.\nSend any float value"

def created_task_fully(lang, ctask):
    if lang == "rus":
        return f"✅ Задание мониторинга курса добавлено!\nДетали созданного задания:\n\n{ctask.ToString()}"
    return f"✅ Currency exchange rates monitoring task has been created.\nDetails of your task:\n\n{ctask.ToString()}"

def created_task_error_pair(lang):
    if lang == "rus":
        return "❌Крипто пара не найдена. Возможно неверно указана или не существует"
    return "❌You have submitted the wrong currency names!"

def created_task_command_only(lang):
    if lang == "rus":
        return "📃 Для создания нового крипто задания отправь мне торговую пару для отслеживания курса (например с биржи binance).\nСначала отправь базовую валюту, например 'BTC', 'LTC', 'ETH'\n\nИли можно отправить полную команду для быстрого создания задания.\nФормат команды:\n/create <базовая валюта> <разменная валюта> <цена> <+ или - для роста или падения цены соответственно>"
    return "📃 To create new monitoring task send me the pair witch you want to monitor.\nFirst send me base currency.\n\nExample: 'BTC' 'LTC' 'ETH' (without quotes)\n\nElse you can send full command like:\n/create <base currency name> <quote> <price> <+ or - for raising price or falling>"

def creation_quote_setted(lang,task):
    if lang == "rus":
        return f"📝 Создание задания\n\n▶️Ваша пара: {task.base}/{task.quote}.\nТеперь отправь цену, по достижению которой будет отправляться уведомление (например '0.05','1200','0.00000312' без кавычек)"
    return f"📝 Task creation\n\n▶️Your pair: {task.base}/{task.quote}.\nNow tell me the price to be reached\n(for example: '0.05', '1200', '0.000002' without quotes)\nWhen this price is reached, an alert will be sent"

def creation_base_setted(lang, base):
    if lang == "rus":
        return f"📝Создание задания.\n\nВыбранная валюта: {base}.\nТеперь выбери разменную валюту для создания пары."
    return f"📝Task creation\n\nYour base currency: {base}. \nNow select quote currency for create pair."

def creation_base_error(lang):
    if lang == "rus":
        return "🚫 Ошибка. Такой валюты не существует"
    return "🚫 Error. You have sent wrong currency name"

def creation_price_setted(lang,ctask):
    if lang == "rus":
        return f"🔰Пара: {ctask.base}/{ctask.quote}.\nЦена:{ctask.price}\nКурс должен 📈 вырасти до такой цены или упасть 📉? Выбери:"
    return f"🔰Pair: {ctask.base}/{ctask.quote}.\nPrice:{ctask.price}\nThe course must 📈 rise to such a price or fall 📉?"

def creation_price_error(lang):
    if lang == "rus":
        return f"❌ Цена неверно указана! Создание задания прервано! Придется начать сначала"
    return f"❌ You have sent wrong value! Task creation aborted! Send /createtask again."

def creation_final_already_have(lang,ctask,olctask):
    if lang == "rus":
        return f"❗️Похожая задача для такой пары уже существует: {ctask.base}/{ctask.quote}.\n{olctask.ToString()}\n\Нужно отредактировать или удалить ее!"
    return f"❗️You already have same task: {ctask.base}/{ctask.quote}.\n{olctask.ToString()}\n\You must edit or delete it!"

def creation_selected(lang):
    if lang == "rus":
        return "🔰Выбрано: "
    return "🔰You have selected: "

def edited_task_info(lang, ctask):
    if lang == "rus":
        return f"🖍 Задание отредактировано! Детали:\n\n{ctask.ToString()}"
    return f"Task edited! Info:\n\n{ctask.ToString()}"

def editting_task(lang,ctask):
    if lang == "rus":
        return f"🖍 Редактирование задания:\n{ctask.ToShortStr()}\nДля редактирования задания пришли новую цену или выбери коэфицент изменения цены для быстрого редактирования./nТакже можно отправть полную команду для быстрого редактирования\n/edit <id> <новая цена>"
    return f"🖍 You are editting pair:\n{ctask.ToShortStr()}.\nFor edit price send the new one or just select price changing factor.\n\nElse you can send /edit <id> <new_price> to fast edit!"

def editting_task_error(lang):
    if lang == "rus":
        return "🚫 Не указан ID.\nДля редактирования задания отправь команду вида:\n\edit <id задания> <новая цена>* - цена опциональна"
    return "🚫 Missing task ID.\nThe command should look like this: \n/edit <task_id> <new_price>* \n* - price is optional"

def id_error(lang):
    if lang == "rus":
        return "🚫Указан неверный ID задания"
    return "🚫You have sent wrong task id!"

def pair_monitoring_enabled(lang, task):
    if lang == "rus":
        return f"✅ Мониторинг {task.ToShortId()} активирован!"
    return f"✅ Pair {task.ToShortId()} is now monitoring!"

def pair_monitoring_disabled(lang, task):
    if lang == "rus":
        return f"❗️ Мониторинг {task.ToShortId()} деактивирован"
    return f"❗️Monitoring disabled for {task.ToShortId()}"

def pair_removed(lang, item):
    if lang == "rus":
        return f"❌ Пара {item.ToShortId()} удалена!"
    return f"❌ Pair ID {item.ToShortId()} removed!"

def check_price(lang):
    if lang == "rus":
        return "🔰Для вывода текущего курса обмена валюты пришли мне пару вида: BTC/USDT где <базовая валюта>/<обменная>"
    return "🔰To check current exchange rates send me currency pair.\n\nFor example: BTC/USDT or RVN/BTC.\nPlease observe this pattern"

def show_by_task_name(lang):
    if lang == "rus":
        return "❗️Вот список заданий с базовой валютой - "
    return "❗️Your list with base - "

def show_by_task_name_err(lang):
    if lang == "rus":
        return "❌У вас нет заданий с такой базовой валютой - "
    return "❌You have no any tasks with such base currency - "

def current_price_pair(lang):
    if lang == "rus":
        return "💸Текущий курс обмена пары "
    return "💸Current price for pair "

def wrong_pair(lang, base, quote):
    if lang == "rus":
        return f"🚫 Пара {base}/{quote} не найдена!"
    return f"🚫I can't find pair {base}/{quote}. Recheck your writting!"

def stop_all_tasks(lang):
    if lang == "rus":
        return "⛔️ Все задания остановлены"
    return "⛔️ All tasks are stopped."

def no_tasks_detected(lang):
    if lang == "rus":
        return "❌ У вас нет ниодного задания для мониторинга!"
    return "❌ You have not added any tasks yet! To add new send /createtask"

def start_all_tasks(lang, ix, alon):
    if lang == "rus":
        alreadyon = f"and {alon-ix} были активированы ранее ✅" if alon-ix>0 else ""
        return f"✅Ваши {ix} заданий активированы, и {alreadyon} "
    alreadyon = f"and {alon-ix} tasks already ON ✅" if alon-ix>0 else ""
    return f"✅Your {ix} monitoring tasks are started and {alreadyon} started \nFor check all your tasks send /showtasks"

def editted_task_info(lang):
    if lang == "rus":
        return "🖍 Задание отредактировано! Инфа:\n\n"
    return "🖍 Task edited! Info:\n\n"

def wrong_value_error(lang):
    if lang == "rus":
        return "❌ Вы отправили неправильное значение!"
    return '❌ You have sent wrong value!'

def all_tasks_removed(lang):
    if lang == "rus":
        return "❌Все задания мониторинга удалены!❌"
    return f"❌Your monitoring list has been fully removed❌"

def action_outdated(lang):
    if lang == "rus":
        return "🚫 Действие устарело!"
    return "🚫 Action is outdated."

def trigger_moved(lang, old_pr, pr, task):
    if lang == "rus":
        return f"\n\n☑️ Триггер уведомления передвинут с {old_pr} на {pr} для {task.ToShortId()}"
    return f"\n\n☑️ Trigger moved from {old_pr} to {pr} for {task.ToShortId()}"

def task_edit_request(lang, task):
    if lang == "rus":
        return f"🖍 Редактирование {task.ToShortStr()}.\nВыбери коэфициент изменения цены или укажи новую"
    return f"🖍 You are editting pair: {task.ToShortStr()}.\nSelect price changing factor or you can set your value."

def task_new_override(lang, task):
    if lang == "rus":
        return f"🖍Задание переписано!\nДетали задания:\n{task.ToString()}"
    return f"Your task overrided. \nDetails of your task:\n{task.ToString()}"

def new_value_set(lang, task):
    if lang == "rus":
        return f"🖍Для установки новой цены для пары {task.ToShortStr()} отправь цену в следующем сообщении!"
    return f"🖍To set a new value for pair {task.ToShortStr()} send it in next message"

def clear_tasks_list_request(lang):
    if lang == "rus":
        return "❌ Вы уверены что хотите очистить список заданий?\nДействие отменить нельзя!"
    return "❌ Are you sure you want to clear the tracking list?\nAction cannot be undone"

def return_rates_tasks(lang):
    if lang == "rus":
        return f"📈📉Ваш список курсов пар, добавленных ранее:\n\n"
    return f"📈📉Your currency exchange rates, based on your tasks: \n\n"

def return_monitoring_list(lang, printer):
    if lang == "rus":
        return f"Ваш список заданий:\n\n{printer}\nЧтобы получить отфильтрованный по базовой валюте список заданий пришли команду следующего вида:\n/show <название валюты>"
    return f"Your monitoring task list:\n\n{printer}\nTo get filtred list by base send: /show <base currency>"

def info_start(lang):
    if lang == "rus":
        return "Привет! Я бот для мониторинга курсов криптовалют. Добавь задания и я отправлю тебе уведомление о увеличении📉 или уменьшении цены📈 до того значения, которое ты выставишь💰.\n📋Список доступных команд ты можешь получить командой: /help\nИнформацию о данном боте🔎: /info"
    return "Hello! I'm crypto currency exchange monitor bot. I can send you 💬 notification when your currency is raise 📉 or fall 📈 to setted value 💰. \nFor create new task 🖍 send: /createtask.\nFor get info 📋 send: /info\nFor get all available commands 🔎 send: /help"