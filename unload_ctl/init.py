#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

s = struct.unpack


class File_Info():
    def __init__(self):
        self.endian = ''  # 平台软件的字节顺序(大小端),0:小端,1:大端
        self.hard = 0  # 用于标识的magic数,4k:0x82,8k:0xa2,16k:0xc2
        self.f_name = ''  # 文件路径
        self.f_no = 0  # 文件号
        self.file = 0
        self.f_type = ''  # 文件类型
        self.blk_size = 0  # 文件的块/页 大小 (B)
        self.blk_sum = 0  # 文件的块/页 总数
        self.DBID = 0  # 数据库ID
        self.SID = ''  # SID,库名
        self.ts_id = 0  # 表空间ID
        self.ts_name = ''  # 表空间名
        self.version = ''  # 版本
        self.big_ts = 0  # 是否是大文件
        self.os = ''  # OS信息
        self.boot = 0  # 启动页


# 解析文件头, block#0
def file_blk_0(data):  # blcock#0
    file_info = File_Info();
    fmt_1 = ''
    if data[1:2] == b'\x02':
        ver_0 = s("2B", data[12:14])
        if ver_0[0] < ver_0[1]:
            file_info.endian = '>';
            fmt_1 = '>'
        elif ver_0[0] > ver_0[1]:
            file_info.endian = '<';
            fmt_1 = '<'
        ver_2 = s(fmt_1 + "2I", data[4:12])
        file_info.blk_size = ver_2[0]
        file_info.blk_sum = ver_2[1]
    else:
        ver_1 = s("<BHI", data[1:8])
        file_info.hard = ver_1[0]
        if ver_1[2] == 49407:
            file_info.endian = 1;
            fmt_1 = '>'
        elif ver_1[2] == 4290772992:
            file_info.endian = 0;
            fmt_1 = '<'
        ver_2 = s(fmt_1 + "2I", data[20:28])
        file_info.blk_size = ver_2[0]
        file_info.blk_sum = ver_2[1]
    return file_info


# 解析文件头, block#1
def file_blk_1(data):  # blcock#1
    file_info = File_Info();
    fmt_1 = ''
    if data[54:55] == b'\x00' and data[24:25] != b'\x00':
        file_info.endian = '>';
        fmt_1 = '>'
    elif data[54:55] != b'\x00' and data[24:25] == b'\x00':
        file_info.endian = '<';
        fmt_1 = '<'
    file_type = {3: 'dbf', 1: 'ctl', 6: 'temp.dbf', 0: 'unknown'}
    data0 = str(data[32:40], encoding="ascii").rstrip(str(b'\x00', encoding="gbk"))  # SID
    data1 = s(fmt_1 + "IQ2H2I2H", data[28:56])
    data2 = s(fmt_1 + "I", data[96:100])
    data3 = s(fmt_1 + "IH", data[332:338])
    data4 = str(data[338:338 + data3[1]], encoding="ascii").rstrip(str(b'\x00', encoding="gbk"))
    ver_1 = s("<4B", data[24:28])  # 版本号
    pagefile = data2[0]  # bootstrap$的起始指针
    file = pagefile // 4194303;
    page = pagefile - 4194303 * file - file  # 页号
    data_1 = s(fmt_1 + "I", data[4:8]);
    file_1 = data_1[0] // 4194303
    if file_1 == 0:
        big_ts = 1
    else:
        big_ts = 0
    type1 = data1[7]
    if type1 not in (1, 3, 6):
        type1 = 0
    if fmt_1 == '>':
        version = str(ver_1[0]) + '.' + str(ver_1[1] // 16) + '.' + str(ver_1[1] % 16) + '.' + str(
            ver_1[2]) + '.' + str(ver_1[3])
    elif fmt_1 == '<':
        version = str(ver_1[3]) + '.' + str(ver_1[2] // 16) + '.' + str(ver_1[2] % 16) + '.' + str(
            ver_1[1]) + '.' + str(ver_1[0])
    data5 = s("B", data[0:1])
    if data5[0] == 21:
        type1 = 1
    file_info.version = version
    file_info.blk_sum = data1[4]
    file_info.blk_size = data1[5]
    file_info.f_no = data1[6]
    file_info.f_type = file_type[type1]
    file_info.big_ts = big_ts
    file_info.SID = data0
    file_info.DBID = data1[0]
    file_info.ts_id = data3[0]
    file_info.ts_name = data4
    file_info.boot = page
    # print("DBID:%d, SID:%s, V:%s\nts_id:%d, ts_name:%s, boot:%d, page_size:%dB "%(data1[0],data0,version,data3[0],data4,page,data1[5]))
    # print("file_no:%d,file_type:%s,page_sum:%d,file_size:%5.2fG\n"%(data1[6],file_type[type1],data1[4],data1[4]*data1[5]/1024/1024/1024))
    return file_info


def unload_ctl(file_info):
    f = file_info.file
    page_size = file_info.blk_size
    if file_info.version[0:2] == '11':
        aa = 31
    elif file_info.version[0:2] == '10':
        aa = 29
    elif file_info.version[0:2] == '8.':
        aa = 15
    f.seek(page_size * aa)
    data1 = f.read(page_size)
    files = []
    frm_1 = file_info.endian + '2H'
    for i in range(32):
        file = File_Info()
        data1_1 = s(frm_1, data1[i * 524 + 20:i * 524 + 24])
        if data1_1[0] not in (3, 4, 7):
            continue
        try:  # 异常处理
            data1_2 = str(data1[i * 524 + 30:i * 524 + 520], encoding="gbk").rstrip(str(b'\x00', encoding="gbk"))
        except UnicodeDecodeError as e:
            print('Err: UnicodeDecodeError:%s' % e)
            data1_2 = ''
        file.f_type = data1_1[0]
        file.f_no = data1_1[1]
        file.f_name = data1_2

        files.append(file)

    return files
