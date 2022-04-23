# -*- coding: utf-8 -*-
# oracle 控制文件 碎片扫描
# B,H,I
import struct

s = struct.unpack


# 记录片段信息：片段号，片段中页数，起始页信息(物理偏移，页号，文件号)，结束页信息(物理偏移，页号，文件号)
class values1:
    def __init__(self):
        self.offset = 0
        self.page_no = 0
        self.file_no = 0


# 记录块信息：块号，块中片段数，起始片段信息(片段编号,起始页号,文件号)，结束片段信息
class values2:
    def __init__(self):
        self.page_sum = 1
        self.file_no_1 = 0
        self.offset_1 = 0
        self.page_no_1 = 0
        self.file_no_2 = 0
        self.offset_2 = 0
        self.page_no_2 = 0


# 异或校验
def ora_page_check_1(data, fmt_1):
    fmt = '<8192h'
    data = s(fmt, data)
    a1 = len(data)
    chk = 0
    for i in range(0, a1):  # 异或校验
        chk = chk ^ data[i]  # 影响i/o
    # print("xor chk: %d " %chk)
    if chk == 0:
        return 1


# 特征值校验
def ora_page_check_2(data, fmt_1):  # data[1] 是版本信息,控制文件件是 0xC2.
    fmt = fmt_1 + '2BHI8B2H'
    data = s(fmt, data[0:20])
    if (data[1] == 0xC2) and data[2] == 0 and (data[0] == 0 or data[0] == 21) and data[3] != 0 and data[13] == 0:
        # data[1]：版本号值(0xC2); data[0]是页面类型; data[3]是块号文件号; data[12]是页校验值; data[2]/data[13]是0000;
        return 1


# 页尾校验
def ora_page_check_3(data, fmt_1):
    if fmt_1 == '>':
        fmt1 = fmt_1 + 'H2B'  # tail
        fmt2 = fmt_1 + '2BHI3HB'  # header
        data1 = s(fmt1, data[16380:16384])
        data2 = s(fmt2, data[0:15])
        if data1[2] == data2[7] and data1[1] == data2[0] and data1[0] == data2[5]:
            # print("tail chk: %d " %chk)
            return 1
    elif fmt_1 == '<':
        fmt1 = fmt_1 + '2BH'
        fmt2 = fmt_1 + '2BHI3HB'
        data1 = s(fmt1, data[16380:16384])
        data2 = s(fmt2, data[0:15])
        if data1[0] == data2[7] and data1[1] == data2[0] and data1[2] == data2[4]:
            # print("tail chk: %d " %chk)
            return 1
