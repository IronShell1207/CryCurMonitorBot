from datetime import datetime, timedelta
import json
import itertools
import os

filename_tasks = "tasklist.json"
filename_usrlist = "userlist.json"

class CryptoTask(object):
    id_iter = itertools.count()
    def __init__(self, 
    id: int = 0, 
    user_id: int = 0, 
    base: str = "", 
    quote: str = '', 
    price: float = 0.0, 
    rofl: bool = False, 
    enable: bool = False):
        self.id = next(CryptoTask.id_iter)
        self.user_id = user_id
        self.base = base
        self.quote = quote
        self.price = price
        self.rofl = rofl
        self.enable = enable
        
    def ToString(self, lng) -> str:
        arr = ">" if self.rofl else "<"
        tred = "📈" if self.rofl else "📉"
        en = '✅' if self.enable==True else '🛑'
        pr = self.price if self.price>0.0001 else "{:^10.8f}".format(self.price)
        if lng == "rus":
            return f"Задание мониторинга обмена курса #{self.id}\nАктивирован: {self.enable}{en}\nБазовая валюта: {self.base}\nОбменная валюта: {self.quote}\nОжидаемая цена: {arr}{pr}{tred}"
        elif lng == "eng":
            return f"Currency monitor task #{self.id}.\n\nEnabled: {self.enable}{en}\nBase currency: {self.base}\nQuote currency: {self.quote}\nWaiting price: {arr}{pr}{tred}"
    
    def ToShortStr(self) -> str:
        arr = ">" if self.rofl else "<"
        tred = "📈" if self.rofl else "📉"
        en = '✅' if self.enable==True else '🛑'
        pr = pr = self.price if self.price>0.0001 else "{:^10.8f}".format(self.price)
        return f" {en} [ID #{self.id}] {self.base}/{self.quote}{arr}{pr}{tred}"

    def ToShortId(self) -> str:
        return f"#{self.id} {self.base}/{self.quote}"

class TaskEncoder(json.JSONEncoder):
    def default(self, Task):
        if isinstance(Task, CryptoTask):
            return {'id': Task.id,
                    'user_id': Task.user_id,
                    "base": Task.base,
                    "quote": Task.quote,
                    "price": Task.price,
                    "rofl": Task.rofl,
                    "enable": Task.enable}
        else:
            super().default(self, Task)
            

class UserEncoder(json.JSONEncoder):
    def default(self, User):
        if isinstance(User, UserSets):
            return {'user_id': User.user_id, 
                    'notifytimer': User.notifytimer, 
                    'notifystyle': User.notifystyle, 
                    'autostartcreate' : User.autostartcreate,
                    'fasteditbtns' : User.fasteditbtns,
                    'notifyonce' : User.notifyonce,
                    'language' : User.language}    
        else:
            super().default(self, User)


def get_json_task_list():
    cryptoData =[]
    if os.path.isfile(filename_tasks):
        fz = open(filename_tasks,'r').read()
        data = json.loads(fz)
        for item in data:
            dag = CryptoTask(id = item['id'],
                             user_id= item['user_id'],
                             base=item['base'],
                             quote=item['quote'],
                             price=item['price'],
                             rofl=item['rofl'],
                             enable=item['enable'])
            cryptoData.append(dag)
    return cryptoData
    

def write_json_tasks(tasklist: list):
    with (open(filename_tasks, 'w')) as writeFile:
        try:
            json.dump(obj=tasklist,cls=TaskEncoder,fp=writeFile,indent=2)
            print(f"{len(tasklist)} tasks writen to {filename_tasks}")
            return True
        except:
            return False
    

def get_json_user_list():
    userList = []
    if os.path.isfile(filename_usrlist):
        fz = open(filename_usrlist,'r').read()
        data = json.loads(fz)
        userList = []
        for usr in data:
            uz = UserSets(user_id=usr['user_id'],
                          notifytimer = usr["notifytimer"],
                          notifystyle = usr['notifystyle'],
                          autostartcreate = usr['autostartcreate'],
                          fasteditbtns =  usr['fasteditbtns'],
                          notifyonce = usr['notifyonce'],
                          language = usr['language'])  
            userList.append(uz)
        return userList
    return userList


def write_json_users(USERlist: list):
    with (open(filename_usrlist, 'w')) as writeFile:
       # try:
        json.dump(obj=USERlist, cls=UserEncoder, fp = writeFile, indent=2)
        print(f"User list updated. Current users count: {len(USERlist)}")
        return True
        #except Exception as en:
        #    print(f"Error! Can't write user list. Check log {en}")
        #    return False
    
    
class UserSets(object):
    def __init__(self, 
                 user_id: int, 
                 notifytimer: int = 90,
                 language: str = "eng",
                 notifystyle: bool = False, 
                 autostartcreate: bool = False, 
                 lastnotify: datetime = datetime.now()-timedelta(minutes=2),
                 fasteditbtns: bool = True,
                 notifyonce: bool = False):
        self.user_id=user_id
        self.notifytimer = notifytimer
        self.notifystyle = notifystyle
        self.autostartcreate = autostartcreate
        self.lastnotify = lastnotify
        self.fasteditbtns = fasteditbtns
        self.notifyonce = notifyonce
        self.language = language