import struct
from decimal import Decimal


class interval(object):  # для словаря
    def __init__(self, left, right):
        self.left = left
        self.right = right


class dictionary_el(object):  # для словаря
    def __init__(self, el_freq, all_let):
        self.el_freq = el_freq
        self.all_let = all_let


class Interval(object):  # для таблицы с интервалами
    def __init__(self, letter, left_border, right_border, res):
        self.letter = letter
        self.left_border = left_border
        self.right_border = right_border
        self.res = res


class letter_data(object):  # для таблицы с частотами

    def __init__(self, letter, quantity, total):
        self.letter = letter
        self.quantity = quantity
        self.total = total


Table = [letter_data(" ", 0, 0)]

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
            Table.append(letter_data(char, 1, 0))
            break

f.close()

for i in range(len(Table)):
    print(Table[i].letter, " - ", Table[i].quantity, " - ", Table[i].total)

print("next")

"""сортировка таблицы"""
i = 1
while i in range(len(Table)):
    j = 1
    while j in range(len(Table) - i - 1):
        if Table[j].quantity < Table[j + 1].quantity:
            z = Table[j]
            Table[j] = Table[j + 1]
            Table[j + 1] = z
        j += 1
    i += 1

index = 1
while index < len(Table):
    Table[index].total = Table[index - 1].total + Table[index].quantity
    index = index + 1

for i in range(len(Table)):
    print(Table[i].letter, " - ", Table[i].quantity, " - ", Table[i].total)

code_data = Interval(None, 0, 65535, "")

first_qtr = (65535 + 1) / 4
half = first_qtr * 2
third_qtr = first_qtr * 3
bits_to_follow = 0
divider = Table[-1].total

f = open(ad, 'r')
for char in f.read():
    index = 0
    while Table[index].letter != char:
        index = index + 1
    l = code_data.left_border
    r = code_data.right_border
    code_data.letter = char
    code_data.left_border = round(l + Table[index - 1].total * (r - l + 1) / divider, 0)
    code_data.right_border = round(l + Table[index].total * (r - l + 1) / divider - 1)
    print(code_data.letter, " - ", code_data.left_border, " - ", code_data.right_border)
    q = 1
    while q == 1:
        q = 0
        if code_data.right_border < half:
            code_data.res += "0"
            q = 1
        elif code_data.left_border >= half:
            code_data.res += "1"
            code_data.left_border -= half
            code_data.right_border -= half
            q = 1
        elif code_data.left_border >= first_qtr and code_data.right_border < third_qtr:
            bits_to_follow += 1
            code_data.left_border -= first_qtr
            code_data.right_border -= first_qtr
            q = 1
        else:
            break
        code_data.left_border += code_data.left_border
        code_data.right_border += code_data.right_border + 1
        print(code_data.left_border, " - ", code_data.right_border, " - ", code_data.res)
f.close()

code_mass = []
FB = 0
free_bits = -1
for i in range(len(code_data.res)):
    if free_bits == -1:
        code_mass.append(0)
        free_bits = 7
    if code_data.res[i] == '1':
        code_mass[-1] = code_mass[-1] | (1 << free_bits)
        free_bits = free_bits - 1
        FB = free_bits
    else:
        free_bits = free_bits - 1
        FB = free_bits

for i in range(len(code_mass)):
    print(code_mass[i])

print(FB)

print("point 1")
"""дальше пошла заготовка для бинарника (не смотреть)"""

Cap = "C:\\ForProg\\ArSortCap.dat"

print("point 2")

f = open(Cap, 'wb')  # открыли файл на запись

print("point 3")

counter = len(Table) * 2  # все, что не код текста
counter = struct.pack('B', counter)
f.write(counter)

print("point 4")

FB += 1
FB = struct.pack('B', FB)
f.write(FB)

print("point 5")

# запись шапки
for i in range(len(Table) - 1):
    p = ord(Table[i].letter)
    if p <= 255:
        w = struct.pack('B', p)
        f.write(w)
        w = struct.pack('I', Table[i].total)
        f.write(w)

print("point 6")

# запись кода
for i in range(len(code_data.res) - 1):
    p = ord(code_data.res[i])
    if p <= 255:
        w = struct.pack('B', p)
        f.write(w)

print("point 7")

f.close()

print("point 8")
