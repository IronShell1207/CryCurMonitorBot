import re

create_re_full = re.compile("/(create|createtask|newtask)\s+(\w{2,5})(\s+|/)(\w{2,4})\s+(\S+)\s+(\+|\-)")
create_re_price = re.compile("/(create|createtask|newtask)\s+(\w{2,5})(\s+|/)(\w{2,4})\s+(\S+)")
create_re_pair = re.compile("/(create|createtask|newtask)\s+(\w{2,5})(\s+|/)(\w{2,4})")
create_univers = re.compile("/(create|createtask|newtask)\s+(\w{2,5})(\s+|/)(\w{2,4})(\s+(\S+)|)(\s+(\+|\-)|)")
#                                       1                       2       3       4       5  6      7    8
edit_re = re.compile("/(edittask|edit|change)\s*(\d+|)(\s([0-9.]+)|)")
                #           1                       2   3  4
pair_re = re.compile(r'(\w{2,5})/(\w{2,5})')
ckpr_pair_re = re.compile(r'/price\s(\w{2,5})/(\w{2,5})')

edit_task_re = re.compile("t/newv(\d+)")

re_value_name = re.compile("([A-Z,a-z]{2,5})")

re_show_tasks = re.compile('/(show|showtasks|display)\s(\w{2,5})')

task_manupulation_re = re.compile('t/(\w+)/(\d+)')
re_fast_value_change = re.compile('t/(\w+)(\d+)/(\d+)')

create_quote_kb = re.compile("n/(\S+)")



text = "/create btc usdt"

recx = create_univers.match(text)
re1 = recx.group(1)
re2 = recx.group(2)
re3 = recx.group(3)
re4 = recx.group(4)
re5 = recx.group(5)
re6 = recx.group(6) # price
re7 = recx.group(7)
re8 = recx.group(8) # rofl