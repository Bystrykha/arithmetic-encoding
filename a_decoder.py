import struct


class table_el(object):
    def __init__(self, letter, total):
        self.letter = letter
        self.total = total


Decode_Table = []
Cap = "C:\\ForProg\\ArSortCap.dat"
f = open(Cap, 'rb')

a = f.read(1)
FB = struct.unpack('B', a)

a = f.read(1)
s = struct.unpack('B', a)

for i in range(s[0]):
    code = struct.unpack('B', f.read(1))
    let = chr(code[0])
    z = f.read(4)
    total = struct.unpack('I', z)
    Decode_Table.append(table_el(let, total))

Decode_Table.insert(0, table_el(None, [0]))

code = f.read()

value = code[0]
value = value << 8
value += code[1]

index = 1
byte = 2
bit = 0

low_border = 0
high_border = 65535
divider = Decode_Table[-1].total[0]
first_qtr = int((high_border + 1) / 4)
half = first_qtr * 2
third_qtr = first_qtr * 3
f = open('C:\ForProg\decode.txt', 'a')

while index < Decode_Table[-1].total[0]:
    low = low_border
    high = high_border
    # print("divider ", divider)
    freq = int(((value - low + 1) * divider - 1) / (high - low + 1))
    j = 1
    while Decode_Table[j].total[0] <= freq:
        j += 1
    # print("value ", value)
    # print("freq ", freq)
    # print("symbol ", Decode_Table[j].letter)
    low_border = int(low + Decode_Table[j - 1].total[0] * (high - low + 1) / divider)
    high_border = int(low + Decode_Table[j].total[0] * (high - low + 1) / divider - 1)
    while 1:
        print("low ", low_border, ", high ", high_border, ", value ", value)
        if high_border < half:
            r = 1
        elif low_border >= half:
            low_border -= half
            high_border -= half
            value -= half
        elif (low_border >= first_qtr) and (high_border < third_qtr):
            low_border -= first_qtr
            high_border -= first_qtr
            value -= first_qtr
        else:
            break
        low_border += low_border
        high_border += high_border + 1
        if byte >= len(code):
            write_bit = 0
        else:
            write_bit = (code[byte] >> (7 - bit)) & 1
        bit += 1
        # print(write_bit)
        if bit == 8:
            byte += 1
            bit = 0
        value += value + write_bit
    f.write(Decode_Table[j].letter)
    index += 1
