import itertools
# import IfcOpenShell
# import sys
# from py2neo import Graph, Node
# import time
# import csv
import copy

list1 = [1, 2, 3]
list2 = copy.copy(list1)
list1.append(4)
print(list1)
print(list2)

dict1 = {'red': 1, 'blue': 2, 'yellow': 30, 'white': 4, 'black': 5}
dict2 = {'red': 43, 'blue': 52, 'yellow': 30, 'white': 54}
dict3 = {'red': 14, 'blue': 23, 'yellow': 30, 'white': 64, 'black': 85}
dict4 = {'red': 43, 'blue': 52, 'yellow': 30, 'white': 54}
dicts = [dict1, dict2, dict3, dict4]

def dict_key_setter(dict_list):
    dict_keys = set(itertools.chain.from_iterable([i.keys() for i in dict_list]))
    for d in dict_list:
        for k in dict_keys:
            d.setdefault(k, "")
    return dict_list

aaa = dict_key_setter(dicts)

print(dict_list)
