import struct
from decimal import Decimal


class interval(object):  # для словаря
    def __init__(self, left, right):
        self.left = left
        self.right = right


class table_el(object):  # для таблицы с интервалами
    def __init__(self, letter, left_border, right_border):
        self.letter = letter
        self.left_border = left_border
        self.right_border = right_border


class letter_data(object):  # для таблицы с частотами

    def __init__(self, letter, quantity):
        self.letter = letter
        self.quantity = quantity


Table = [letter_data(" ", 0)]

all_letters = 0

ad = "C:\ForProg\AS.txt"

"""читаем текст и составляем таблицу с данными о символах"""

f = open(ad, 'r')
for char in f.read():
    all_letters = all_letters + 1
    for j in range(len(Table)):
        if char == Table[j].letter:
            Table[j].quantity = Table[j].quantity + 1
            break
        if j == len(Table) - 1:
            Table.append(letter_data(char, 1))
            break

f.close()

"""сортировка таблицы"""
for i in range(len(Table)):
    for j in range(len(Table) - i - 1):
        if Table[j].quantity < Table[j + 1].quantity:
            z = Table[j]
            Table[j] = Table[j + 1]
            Table[j + 1] = z

i = 0

Coding_table = []

for i in range(len(Table) - 1):  # составили таблицу типа: буква - левая граница - правая граница
    if i == 0:
        left = 0
    else:
        left = Coding_table[i - 1].right_border
    right = (Table[i].quantity / all_letters) + left
    Coding_table.append(table_el(Table[i].letter, left, right))

dictionary = dict()
for i in range(len(Coding_table)):
    dictionary[Coding_table[i].letter] = interval(Coding_table[i].left_border, Coding_table[i].right_border)

code_txt = interval(0.0, 1.0)

f = open(ad, 'r')
for char in f.read():
    high = code_txt.right
    low = code_txt.left
    code_txt.right = low + (high - low) * dictionary[char].right
    code_txt.left = low + (high - low) * dictionary[char].left
    str_l = str(code_txt.left)
    str_r = str(code_txt.right)
    if ord(str_r[2]) == ord(str_l[2]):
        str_r.index('.')
        print(str_r[2], " - ", str_l[2])
        a = str_r[2]
        str_r.replace(a, '0', 1)
        str_l.replace(a, '0', 1)
        code_txt.right = float(str_r) * 10
        code_txt.left = float(str_l) * 10
    print(code_txt.left, " - ", code_txt.right)

f.close()

# str_l = str(code_txt.left)
# print(str_l)
# print(str_l[0], str_l[1], str_l[2], str_l[3])
# print(ord(str_l[0]), ord(str_l[1]), ord(str_l[2]))
# a = str_l[2]
# print(a)
# str_l = str_l.replace(a, '0', 1)
# print(str_l)







