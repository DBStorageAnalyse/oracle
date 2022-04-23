# -*- coding: utf-8 -*-
# 计算页面的校验值
import struct

s = struct.unpack  # B H I


# 数据文件，控制文件，redo.log文件 的校验值
def ora_page_check_1(data, fmt_1):
    page_size = len(data)
    if page_size == 512:
        a0 = 14
    else:
        a0 = 16
    chk0 = s('<h', data[16:18])
    data = data[0:a0] + data[a0 + 2:page_size]
    fmt = '%s%dh' % (fmt_1, len(data) / 2)
    data1 = s(fmt, data)

    a1 = len(data1)
    chk = 0
    for i in range(0, a1):  # 异或校验
        chk = chk ^ data1[i]
    if chk < 0:
        chk = 65536 + chk
    aa = hex(chk).upper()
    if len(aa) < 6:
        a1 = '0' * (6 - len(aa))
        aa = '0x' + a1 + aa[2:len(aa)]
    if fmt_1 == '<':
        print("chk: %s to %s --> 0x %s %s " % (hex(chk0[0]), hex(chk), aa[4:6], aa[2:4]))
    elif fmt_1 == '>':
        print("chk: %s to %s --> 0x %s %s " % (hex(chk0[0]), hex(chk), aa[2:4], aa[4:6]))
    return chk


# ASM 元文件的页面校验值
def ora_page_check_2(data, fmt_1):
    page_size = 4096;
    a0 = 12
    data = data[0:a0] + data[a0 + 4:page_size]
    fmt = '%s%dI' % (fmt_1, len(data) / 4)
    data1 = s(fmt, data)
    a1 = len(data1)
    chk = 0
    for i in range(0, a1):  # 异或校验
        chk = chk ^ data1[i]
    if chk < 0:
        chk = 4294967295 + chk
    aa = hex(chk).upper()
    if len(aa) < 6:
        a1 = '0' * (6 - len(aa))
        aa = '0x' + a1 + aa[2:len(aa)]
    if fmt_1 == '<':
        print("chk: %s --> %s %s %s %s " % (hex(chk), aa[8:10], aa[6:8], aa[4:6], aa[2:4]))
    elif fmt_1 == '>':
        print("chk: %s --> %s %s %s %s " % (hex(chk), aa[2:4], aa[4:6], aa[6:8], aa[8:10]))
    return chk


def hex_view(data):
    fmt = '%dB' % (len(data))
    data1 = s(fmt, data)
    print(' \t| 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15')
    print('-------------------------------------------------------|-------------------')
    for i in range(len(data) // 16):
        ss = '';
        ss2 = ''
        for ii in range(16):
            aa = hex(data1[i * 16 + ii]).upper()
            data2 = data[i * 16 + ii:i * 16 + ii + 1]
            data3 = s('B', data2)
            if data3[0] >= 128 or data3[0] == 10:
                data2 = b'\x00'
            bb = str(data2, encoding="ascii")
            if len(aa) < 4:
                a1 = '0' * (4 - len(aa))
                aa = a1 + aa[2:len(aa)]
            elif len(aa) == 4:
                aa = aa[2:4]
            if ii == 7:
                aa = aa + ' '
            ss += aa + ' '
            ss2 += bb
        print('%d\t| %s| %s |' % (i, ss, ss2))


fmt_1 = '<'
page_size = 16384  # 16384  8192  512
f_name = r'C:\Users\zsz\Desktop\control01.ctl'
f = open(f_name, 'rb')
f.seek(page_size * 32)
data = f.read(page_size)
ora_page_check_1(data, fmt_1)  # 数据文件，控制文件，redo.log文件 的校验值
# ora_page_check_2(data,fmt_1)  # ASM 元文件的页面校验值
# hex_view(data)
