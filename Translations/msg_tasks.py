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
        return f"Похожая задача для такой пары уже существует: {ctask.base}/{ctask.quote}.\n{olctask.ToString()}\n\Нужно отредактировать или удалить ее!"
    return f"You already have same task: {ctask.base}/{ctask.quote}.\n{olctask.ToString()}\n\You must edit or delete it!"

def creation_selected(lang):
    if lang == "rus":
        return "Выбрано: "
    return "You have selected: "

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