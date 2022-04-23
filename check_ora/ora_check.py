# -*- coding: utf-8 -*-
# oracle page_check
import struct, ctypes

s = struct.unpack  # B,H,I
# 异或校验

dll = ctypes.windll.LoadLibrary('OracleCheckSum.dll')


def ora_page_check_1(data, fmt_1):
    a1 = len(data)
    chk = dll.OracleCheck(data, a1)
    if chk == 0:
        return 1
    else:
        return 0


# 特征值校验
def ora_page_check_2(data, fmt_1):  # data[1] 是版本信息0xA2
    fmt = fmt_1 + '2BHI8B2H'
    len_1 = len(data)
    magic = {512: 0x22, 1024: 0x42, 2048: 0x62, 4096: 0x82, 8192: 0xa2, 16384: 0xc2, 32768: 0xe2}
    # 512B:0x22,1k:0x42,2k:0x62,4k:0x82,8k:0xa2,16k:0xc2,32k:0xe2
    data = s(fmt, data[0:20])
    if (data[1] == magic[len_1] or data[1] == 2) and data[2] == 0 and data[3] != 0 and data[13] == 0:
        return 1
    else:
        return 0


# 页尾校验
def ora_page_check_3(data, fmt_1):
    len_1 = len(data)
    if fmt_1 == '>':
        fmt1 = fmt_1 + 'H2B'  # tail
        fmt2 = fmt_1 + '2BHI3HB'  # header
        data1 = s(fmt1, data[len_1 - 4:len_1])
        data2 = s(fmt2, data[0:15])
        if data1[2] == data2[7] and data1[1] == data2[0] and data1[0] == data2[5]:
            return 1
        else:
            return 0
    elif fmt_1 == '<':
        fmt1 = fmt_1 + '2BH'
        fmt2 = fmt_1 + '2BHI3HB'
        data1 = s(fmt1, data[len_1 - 4:len_1])
        data2 = s(fmt2, data[0:15])
        if data1[0] == data2[7] and data1[1] == data2[0] and data1[2] == data2[4]:
            return 1
        else:
            return 0


# 数据文件，控制文件，redo.log文件 的校验值
def ora_page_chk_1(data, fmt_1, page_size):
    if page_size == 512:  # redo log
        a0 = 14
    else:  # 数据文件，控制文件
        a0 = 16
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
        print("chk: %s --> %s %s " % (hex(chk), aa[4:6], aa[2:4]))
    elif fmt_1 == '>':
        print("chk: %s --> %s %s " % (hex(chk), aa[2:4], aa[4:6]))
    return chk


# ASM 元文件的页面校验值
def ora_page_chk_2(data, fmt_1, page_size):
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

# ora_page_chk_1(data,fmt_1,page_size)    # 数据文件，控制文件，redo.log文件 的校验值
# ora_page_chk_2(data,fmt_1,page_size)  # ASM 元文件的页面校验值
