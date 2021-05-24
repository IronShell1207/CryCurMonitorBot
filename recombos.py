import re

create_re_full = re.compile("/(create|createtask|newtask)\s+(\w{2,5})(\s+|/)(\w{2,4})\s+(\S+)\s+(\+|\-)")
create_re_price = re.compile("/(create|createtask|newtask)\s+(\w{2,5})(\s+|/)(\w{2,4})\s+(\S+)")
create_re_pair = re.compile("/(create|createtask|newtask)\s+(\w{2,5})(\s+|/)(\w{2,4})")