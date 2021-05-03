import json
import itertools
import os

filename = "tasklist.json"

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
    
    def ToString(self) -> str:
        arr = ">" if self.rofl else "<"
        pr = self.price if self.price>1 else "{:^10.8f}".format(self.price)
        return f"Currency monitor task #{self.id}.\n\nEnabled: {self.enable}\nBase currency: {self.base}\nQuote currency: {self.quote}\nWaiting for price: {arr}{pr}"
    
    def ToShortStr(self) -> str:
        arr = ">" if self.rofl else "<"
        en = 'enabled' if self.enable==True else 'disabled'
        pr = pr = self.price if self.price>1 else "{:^10.8f}".format(self.price)
        return f"Task ID #{self.id} for pair {self.base}/{self.quote} with limit {arr}{pr} is {en}"

class TaskEncoder(json.JSONEncoder):
    def default(self, Task):
        if isinstance(Task, CryptoTask):
            return {'id': Task.id,'user_id': Task.user_id,"base": Task.base,"quote": Task.quote,"price": Task.price,"rofl": Task.rofl,"enable": Task.enable}
        else:
            super().default(self, Task)
            
    
def get_json_task_list():
    if os.path.isfile(filename):
        fz = open(filename,'r').read()
        data = json.loads(fz)
        cryptoData =[]
        for item in data:
            dag = CryptoTask(id = item['id'],
                             user_id= item['user_id'],
                             base=item['base'],
                             quote=item['quote'],
                             price=item['price'],
                             rofl=item['rofl'],
                             enable=False)
            cryptoData.append(dag)
        return cryptoData
    
def write_json_tasks(tasklist: list):
    with (open(filename, 'w')) as writeFile:
        try:
            json.dump(obj=tasklist,cls=TaskEncoder,fp=writeFile,indent=2)
            print(f"{len(tasklist)} tasks writen to {filename}")
            return True
        except:
            return False
    