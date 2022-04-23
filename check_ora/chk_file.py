#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, os.path, struct  # ,threading
from PyQt5.QtCore import QThread, pyqtSignal
import ora_check

s = struct.unpack  # B H I


class File_Info():
    def __init__(self):
        self.endian = 0  # 平台软件的字节顺序(大小端),0:小端,1:大端
        self.hard = 0  # 用于标识的magic数,4k:0x82,8k:0xa2,16k:0xc2
        self.f_name = ''
        self.f_size = 0
        self.f_no = 0  # 文件号
        self.f_type = ''  # 文件类型
        self.blk_size = 8192  # 文件的块/页 大小 (B)
        self.blk_sum = 0  # 文件的块/页 总数
        self.scan_sum = 0  # 扫描的真实的块/页 总数
        self.start_pg_no = 0  # 起始页号
        self.start_no = 0  # 文件开始检测的物理块号
        self.DBID = 0
        self.version = ''
        self.SID = ''
        self.ts_id = 0
        self.ts_name = ''
        self.big_ts = 0  # 是否是大文件
        self.file_create_scn = 0
        self.chkpoint_scn = 0
        self.err_pages = []  # 损坏的块


class Err_Page():
    def __init__(self):
        self.blk_no = 0
        self.rdba = 0
        self.page_type = 0
        self.chk_err = ''


def file_blk_1(data):  # blcock#1
    file_info = File_Info();
    fmt_1 = '';
    version = ''
    if data[54:55] == b'\x00' and data[24:25] != b'\x00':
        file_info.endian = 1;
        fmt_1 = '>'
    elif data[54:55] != b'\x00' and data[24:25] == b'\x00':
        file_info.endian = 0;
        fmt_1 = '<'
    file_type = {3: 'dbf', 1: 'ctl', 6: 'temp.dbf', 0: 'unknown'}
    data0 = str(data[32:40], encoding="ascii").rstrip(str(b'\x00', encoding="gbk"))  # SID
    data1 = s(fmt_1 + "IQ2H2I2H", data[28:56])
    data2 = s(fmt_1 + "2I", data[96:104])
    data3 = s(fmt_1 + "IH", data[332:338])
    data4 = str(data[338:338 + data3[1]], encoding="ascii").rstrip(str(b'\x00', encoding="gbk"))
    data5 = s(fmt_1 + "I", data[484:488])
    ver_1 = s("<4B", data[24:28])
    file_create_scn = data2[1]
    chkpoint_scn = data5[0]
    pagefile = data2[0]  # bootstrap$的起始指针
    file = pagefile >> 22;
    page = pagefile - 4194303 * file - file  # 页号
    data_1 = s(fmt_1 + "I", data[4:8]);
    file_1 = data_1[0] >> 22
    if file_1 == 0:
        big_ts = 1
    else:
        big_ts = 0
    type1 = data1[7]
    if fmt_1 == '>':
        version = str(ver_1[0]) + '.' + str(ver_1[1] // 16) + '.' + str(ver_1[1] % 16) + '.' + str(
            ver_1[2]) + '.' + str(ver_1[3])
    elif fmt_1 == '<':
        version = str(ver_1[3]) + '.' + str(ver_1[2] // 16) + '.' + str(ver_1[2] % 16) + '.' + str(
            ver_1[1]) + '.' + str(ver_1[0])
    if type1 not in (1, 3, 6):
        type1 = 0
    data5 = s("B", data[0:1])
    if data5[0] == 21:
        type1 = 1;
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
    file_info.file_create_scn = file_create_scn
    file_info.chkpoint_scn = chkpoint_scn

    # print("DBID:%d, SID:%s, V:%s\nts_id:%d, ts_name:%s, boot:%d, page_size:%dB "%(data1[0],data0,version,data3[0],data4,page,data1[5]))
    # print("file_no:%d,file_type:%s,page_sum:%d,file_size:%5.2fG\n"%(data1[6],file_type[type1],data1[4],data1[4]*data1[5]/1024/1024/1024))
    return file_info, page


def file_blk_0(data):  # blcock#0
    file_info = File_Info();
    fmt_1 = ''

    if data[1:2] == b'\x02':  # 8i/9i
        ver_0 = s("2B", data[12:14])
        if ver_0[0] < ver_0[1]:
            file_info.endian = 1;
            fmt_1 = '>'
        elif ver_0[0] > ver_0[1]:
            file_info.endian = 0;
            fmt_1 = '<'
        ver_2 = s(fmt_1 + "2I", data[4:12])
        if ver_2[0] in (1024, 2018, 4096, 8192, 16384):
            file_info.start_pg_no = 0
        else:
            file_info.start_pg_no = ver_2[0]
        file_info.blk_size = ver_2[0]
        file_info.blk_sum = ver_2[1]
    elif data[1:2] == b'\x00':  # 8i/9i
        return file_info
    else:
        ver_0 = s("<H", data[4:6])
        if ver_0[0] > 16384:
            file_info.endian = 1;
            fmt_1 = '>'
            ver_3 = s(">H", data[6:8])
            file_info.start_pg_no = ver_3[0]
        elif ver_0[0] < 16384:
            file_info.endian = 0;
            fmt_1 = '<'
            file_info.start_pg_no = ver_0[0]
        ver_2 = s(fmt_1 + "2I", data[20:28])
        file_info.blk_size = ver_2[0]
        file_info.blk_sum = ver_2[1]
    return file_info


# 文件信息
def f_info(f_name):
    f = open(f_name, 'rb')
    page = 0
    data = f.read(32)
    file_info = file_blk_0(data)
    start_pg_no = file_info.start_pg_no
    if start_pg_no == 0:
        off_start = file_info.blk_size
    elif start_pg_no == 1:
        off_start = 0
    else:
        return file_info, page
    f.seek(off_start)
    data = f.read(512)
    file_info, page = file_blk_1(data)
    file_info.f_name = f_name
    file_info.start_pg_no = start_pg_no
    file_info.f_size = os.path.getsize(f_name)
    f.close()
    return file_info, page


# 多线程,文件扫描
class SCAN(QThread):  # 类ORA_SCAN继承自 QThread
    PUP = pyqtSignal(int)  # 更新进度条的信号
    LUP = pyqtSignal(str)

    def __init__(self, parent=None):  # file_info文件信息，start扫描起始偏移，level是检测的严格程度
        super(SCAN, self).__init__(parent)
        self.file_info = []
        self.start_no = 0
        self.level = 0
        self.err_pages = []

    # 检测文件所有页, 单独开的线程
    def run(self):  # file_info文件信息，start扫描起始偏移，level是检测的严格程度
        f_name = self.file_info.f_name;
        endian = self.file_info.endian;
        page_size = self.file_info.blk_size
        f = open(f_name, 'rb')
        start1 = self.start_no * 8192  # 扫描起始偏移
        f_size = os.path.getsize(f.name) - start1
        begin = time.time()
        print("开始检测:%s \t大小:%5.1f M" % (f.name, f_size / 1024 / 1024))
        buff_size = 8 * 1024 * 1024  # baffer大小
        loop_1 = f_size // buff_size
        loop_1_1 = f_size % buff_size
        loop_2 = buff_size // page_size
        loop_2_1 = loop_1_1 // page_size
        self.file_info.scan_sum = f_size // page_size
        if endian == 1:  # 大端
            fmt_1 = '>'
        elif endian == 0:  # 小端
            fmt_1 = '<'
        chk1_1 = {1: '', 0: 'hash,'};
        chk2_1 = {1: '', 0: '页头校验,'};
        chk3_1 = {1: '', 0: '页尾检验,'};
        chk4_1 = {1: '', 0: 'RDBA,'}
        for i in range(0, loop_1 + 1):
            f.seek(i * buff_size + start1)
            data = f.read(buff_size)
            self.PUP.emit(i + 1)
            self.LUP.emit(" Percent:%5.1f%%" % (((i + 1) / (loop_1 + 1)) * 100))
            print("Buffer:%d/%d; Percent:%5.1f%% \r" % (i, loop_1, ((i + 1) / (loop_1 + 1)) * 100), end="")
            if (i < loop_1):  # 处理文件的所有buffer块
                for ii in range(0, loop_2):
                    pos1 = ii * page_size
                    data1 = data[pos1:pos1 + page_size]
                    fmt = fmt_1 + '2BHI'
                    data2 = s(fmt, data1[0:8])
                    pagefile = data2[3]
                    file = pagefile >> 22
                    page = pagefile - 4194303 * file - file
                    if file == 1023:
                        file = self.file_info.f_no
                    if self.level == 0:  # level 是检测的严格程度
                        chk1 = 1
                    elif self.level == 1:
                        chk1 = ora_check.ora_page_check_1(data1, fmt_1)  # 异或校验，慢
                    chk2 = ora_check.ora_page_check_2(data1, fmt_1)  # 特征值校验
                    chk3 = ora_check.ora_page_check_3(data1, fmt_1)  # 页尾校验
                    if data2[0] == 0 and data2[1] == 2 and file == 0:  # oracle 8的 block#0
                        page = 0;
                        file = self.file_info.f_no;
                        chk1 = 1;
                        chk3 = 1
                    if page == i * loop_2 + ii + self.file_info.start_pg_no + self.start_no:  # and file == self.file_info.f_no  # 没检验文件号
                        chk4 = 1  # RDBA
                    else:
                        chk4 = 0
                    if chk2 != 1 or chk3 != 1 or chk1 != 1 or chk4 != 1:  # 损坏页
                        chk = chk2_1[chk2] + chk3_1[chk3] + chk1_1[chk1] + chk4_1[
                            chk4]  # 校验结果: 特征值 + 页尾校验 + 异或 + RDBA (1:正常,0:不正常)
                        err_page = Err_Page()
                        err_page.blk_no = i * loop_2 + ii
                        err_page.rdba = str(page) + '/' + str(file)
                        err_page.chk_err = chk
                        err_page.page_type = data2[0]
                        self.err_pages.append(err_page)
            elif (i == loop_1):  # 处理文件尾部不足buffer的块
                for ii in range(0, loop_2_1):
                    off_set = i * buff_size + ii * page_size
                    if off_set > f_size - page_size:
                        break
                    pos1 = ii * page_size
                    data1 = data[pos1:pos1 + page_size]
                    fmt = fmt_1 + '2BHI'
                    data2 = s(fmt, data1[0:8])
                    pagefile = data2[3]
                    file = pagefile >> 22
                    page = pagefile - 4194303 * file - file
                    if file == 1023:
                        file = self.file_info.f_no
                    if self.level == 0:  # level 是检测的严格程度
                        chk1 = 1
                    elif self.level == 1:
                        chk1 = ora_check.ora_page_check_1(data1, fmt_1)  # 异或校验
                    chk2 = ora_check.ora_page_check_2(data1, fmt_1)  # 特征值
                    chk3 = ora_check.ora_page_check_3(data1, fmt_1)  # 页尾校验
                    if data2[0] == 0 and data2[1] == 2 and file == 0:  # oracle 8的 block#0
                        page = 0;
                        file = self.file_info.f_no;
                        chk1 = 1;
                        chk3 = 1
                    if page == i * loop_2 + ii + self.file_info.start_pg_no + self.start_no:  # and file == self.file_info.f_no
                        chk4 = 1  # RDBA
                    else:
                        chk4 = 0
                    if chk2 != 1 or chk3 != 1 or chk1 != 1 or chk4 != 1:  # 损坏页
                        chk = chk2_1[chk2] + chk3_1[chk3] + chk1_1[chk1] + chk4_1[
                            chk4]  # 校验结果: 特征值 + 页尾校验 + 异或 + RDBA (1:正常,0:不正常)
                        err_page = Err_Page()
                        err_page.blk_no = i * loop_2 + ii
                        err_page.rdba = str(page) + '/' + str(file)
                        err_page.chk_err = chk
                        err_page.page_type = data2[0]
                        self.err_pages.append(err_page)
        f.close()
        print("\nFile size:%6.2f G, I/O:%4.1f M/s\n" % (
        f_size / 1024 / 1024 / 1024, f_size / 1024 / 1024 / (time.time() - begin)))  # I/O

    def get_return(self):
        return self.err_pages
