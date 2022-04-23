#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  oracle 控制文件的碎片扫描. 支持大小端存储 ， 控制文件的连续性比较好
import struct, sqlite3, time
import ctl_check

s = struct.unpack


def ora_scan(f_name, db_name, start_off, end_off, endian, scan_size):
    # f 是要扫描的文件，start 扫描的起始字节偏移，db_name是输出的数据库路径
    begin = time.time()
    print("Datetime: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin)))  # current time
    print('f_name:%s, db_name:%s ' % (f_name, db_name))
    f = open(f_name, 'rb')
    f1 = open(db_name, 'wb');
    f1.close()  # 打开sqlite数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()  # 数据库游标
    cursor.execute(" create table ora_page(id integer primary key,offset,page_type,file_no,page_no,chk)")
    scan_size = scan_size  # 扫描 的 步长 ,精度, 影响I/O速度
    buff_size = 32 * 1024 * 1024  # baffer大小，2M(有点小) 8M,  32M
    page_size = 16384  # 页面大小16K
    f_size = end_off - start_off
    loop_1 = f_size // buff_size
    loop_1_1 = f_size % buff_size
    loop_2 = buff_size // scan_size
    loop_2_1 = loop_1_1 // scan_size
    sum = 0;
    page_0 = 0;
    page_15 = 0

    if endian == 1:  # 大端
        fmt_1 = '>'
    elif endian == 0:  # 小端
        fmt_1 = '<'

    for i in range(0, loop_1 + 1):  # 处理文件的所有buffer块
        f.seek(i * buff_size + start_off)
        data = f.read(buff_size + page_size)

        if (i < loop_1):  # 处理文件的所有buffer块
            for ii in range(0, loop_2):
                pos1 = ii * scan_size  #
                data1 = data[pos1:pos1 + page_size]
                fmt = fmt_1 + '2BHI8B2H'
                data2 = s(fmt, data1[0:20])
                # chk1 = ctl_check.ora_page_check_1(data1,fmt_1)
                # chk3 = ctl_check.ora_page_check_3(data1,fmt_1)
                chk2 = ctl_check.ora_page_check_2(data1, fmt_1)
                if chk2 == 1:
                    chk3 = ctl_check.ora_page_check_3(data1, fmt_1)
                    if chk3 == 1:
                        chk1 = 1  # ctl_check.ora_page_check_1(data1,fmt_1)
                        if chk1 == 1:
                            if data2[0] == 0:
                                page_0 += 1
                            elif data2[0] == 0x15:
                                page_15 += 1
                            sum += 1
                            # print("find a page ！")
                            off_set = i * buff_size + ii * scan_size
                            pagefile = data2[3]
                            file = pagefile >> 22
                            page = pagefile - 4194303 * file - file
                            ii += page_size / scan_size
                            cursor.execute(
                                "insert into ora_page(offset,page_type,file_no,page_no,chk) values(?,?,?,?,?)",
                                (off_set, data2[0], file, page, data2[12]))
                            if sum % 10000 == 0:
                                conn.commit()  # 每32 M commit一次, 影响Ｉ／Ｏ速度　

        elif (i == loop_1):  # 处理文件尾部不足buffer的块
            for ii in range(0, loop_2_1):
                pos1 = ii * scan_size  #
                data1 = data[pos1:pos1 + page_size]
                fmt = fmt_1 + '2BHI8B2H'
                data2 = s(fmt, data1[0:20])
                off_set = i * buff_size + ii * scan_size  # ========
                if off_set > f_size:
                    break
                chk2 = ctl_check.ora_page_check_2(data1, fmt_1)
                if chk2 == 1:
                    chk3 = ctl_check.ora_page_check_3(data1, fmt_1)
                    if chk3 == 1:
                        chk1 = 1  # ctl_check.ora_page_check_1(data1,fmt_1)
                        if chk1 == 1:
                            if data2[0] == 0:
                                page_0 += 1
                            elif data2[0] == 0x15:
                                page_15 += 1
                            sum += 1

                            pagefile = data2[3]
                            file = pagefile >> 22
                            page = pagefile - 4194303 * file - file
                            ii += page_size / scan_size
                            cursor.execute(
                                "insert into ora_page(offset,page_type,file_no,page_no,chk) values(?,?,?,?,?)",
                                (off_set, data2[0], file, page, data2[12]))

        if i % (loop_1 // 1000 + 1) == 0 or i == loop_1:  # 输出扫描进度
            progress = ((i + 1) / (loop_1 + 1)) * 100
            print("Buffer:%d/%d; Percent:%5.1f%%; Find:%d \r" % (i, loop_1, progress, sum), end="")

    print("总页数: %d, 空页数: %d, 数据页: %d " % (sum, page_0, page_15))  # 总页数,空页数,数据页数

    cursor.close()
    conn.commit()
    conn.close()
    f.close()
    end = time.time()
    print("Datetime: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end)), end='')  # current time
    print("\t Used time: %d:" % ((end - begin) // 3600) + time.strftime('%M:%S', time.localtime(end - begin)))  # 用时
    print("File size: %6.2f G, I/O: %4.1f M/s" % (
    f_size / 1024 / 1024 / 1024, f_size / 1024 / 1024 / (end - begin)))  # I/O

# return file_infos

# f_name = r'C:\Users\zsz\PycharmProjects\oracle\test\control_big.ctl'
# db_name = r'C:\Users\zsz\PycharmProjects\oracle\test\control_big.db'
# ora_scan(f_name,0,1,db_name)  # f 是要扫描的文件，start 扫描的起始字节偏移，db_name是输出的数据库路径
