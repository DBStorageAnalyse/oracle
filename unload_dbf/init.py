#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 有系统表的从系统表中读取表结构信息放到sqlite中(或不取),没有系统表的从sql文件或ini文件中获取系统表信息存储到sqlite中
import sqlite3, struct
import table_struct, page

s = struct.unpack


def file_blk_0(data):  # blcock#0
    file_info = table_struct.File_Info();
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
    elif data[1:2] == b'\x00':  # 8i/9i
        return file_info
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
    file_info = table_struct.File_Info();
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


# global db1
db1 = table_struct.st_db()


def init_sys_tab(file_info):  # 初始化 db1
    # 读取sqlite数据库表，获得配置信息 和 系统表的表结构信息
    db = './db_info.db'  # 数据库文件名称
    conn = sqlite3.connect(db)  # 打开数据库
    cursor = conn.cursor()
    cursor.execute("select * from tab_info order by id ")
    values_tab = cursor.fetchall()  # 返回数据为二维数组
    db1.version = file_info.version
    db1.endian = file_info.endian
    db1.page_size = file_info.blk_size
    db1.db_name = file_info.SID
    db1.db_id = file_info.DBID
    db1.os = file_info.os
    for i in range(len(values_tab)):  # 初始化表结构
        table1 = table_struct.st_table()
        table1.tab_obj_id = values_tab[i][1]
        table1.bobj = values_tab[i][2]
        table1.tab_no = values_tab[i][3]
        table1.tab_type = values_tab[i][4]
        table1.tab_name = values_tab[i][5]
        table1.col_sum = values_tab[i][6]
        cursor.execute(
            "select c.* from tab_info t,col_info c where c.tab_obj_id = t.tab_obj_id and t.tab_obj_id=%d order by c.col_id " % (
                table1.tab_obj_id))  # %table1.tab_obj_id
        values_col = cursor.fetchall()
        if len(values_col) == 0:
            table1.col_sum = 0
        for ii in range(0, table1.col_sum):
            column1 = table_struct.st_column()
            column1.tab_obj_id = values_col[ii][1]
            column1.col_id = values_col[ii][2]
            column1.col_name = values_col[ii][3]
            column1.col_type = values_col[ii][4]
            column1.col_len = values_col[ii][5]
            table1.col.append(column1)
        if table1.bobj == 2:
            db1.tab1.append(table1)
        elif table1.bobj == 10:
            db1.tab2.append(table1)
        elif table1.bobj == 0:
            db1.tab0.append(table1)
        if db1.version.find('10', 0, -1) >= 0:
            db1.tab0[0].tab_obj_id = 56
    cursor.close()
    conn.close()


def seg_unload(file_infos, file_no, page_no):
    ext = [];
    f = 0
    pos1 = (page_no) * db1.page_size
    for f_info in file_infos:
        if f_info.f_no == file_no:
            f = f_info.file
            break
    if page_no == 0 or f == 0:
        return ext, 0, 0
    f.seek(pos1)  # 要判断返回值，是否成功
    data = f.read(db1.page_size)
    data1 = s(db1.endian + '2I', data[36:44])
    ext_sum = data1[0]
    blk_sum = data1[1]
    frm = db1.endian + str(ext_sum * 2) + 'I'
    if file_no != 1:
        try:
            data2 = s(frm, data[280:280 + ext_sum * 8])
        except struct.error:
            print('ext_sum 溢出。。%d' % page_no)
            return ext, ext_sum, blk_sum
    elif file_no == 1:
        data2 = s(frm, data[108:108 + ext_sum * 8])
    for i in range(0, ext_sum * 2, 2):
        ext1 = table_struct.st_ext()
        pagefile = data2[i]
        file = pagefile >> 22;
        page = pagefile - 4194303 * file - file  # 页号
        ext1.dba_off_f = file;
        ext1.dba_off_b = page
        ext1.dba_sum = data2[i + 1]
        ext.append(ext1)
    return ext, ext_sum, blk_sum


# 解析 普通表
def page_unload_1(file_infos, table):  # 文件，要解析的页链的起始页面号，表
    print('解析普通表：%s ======= page_no: %d =======' % (table.tab_name, table.page_no))
    tab_data = [];
    blk_sum = 0
    for i in range(len(table.ext)):
        if i == 0 and table.file_no == 1:
            a = 1
        if i == 0 and table.tab_name == 'bootstrap$':
            a = 0
        elif i == 0 and table.file_no != 1:
            a = 3
        elif i != 0:
            a = 0
        for f_info in file_infos:
            if f_info.f_no == table.file_no:
                f = f_info.file
                break
        for ii in range(a, table.ext[i].dba_sum):  # 解析数据段里的所有页面
            if blk_sum >= table.blkcnt:
                break
            pos1 = (table.ext[i].dba_off_b + ii) * db1.page_size
            f.seek(pos1)  # 要判断返回值，是否成功
            data = f.read(db1.page_size)
            data1 = data[0:db1.page_size]
            page1 = page.record1(db1, data1, table, file_infos)  # 解析页面记录.  ***************
            tab_data.append(page1)
            blk_sum += 1
            if f_info.f_no > 1 and blk_sum > 100:  # 只解析一部分数据  有问题
                break
    return tab_data


# 解析cluster表
def page_unload_2(file_infos, table):
    print('解析聚簇表：%s ======= page_no: %d =======' % (table[0].tab_name, table[0].page_no))
    tab_data = [];
    blk_sum = 0
    for i in range(len(table[0].ext)):
        for f_info in file_infos:
            if f_info.f_no == table[0].file_no:
                f = f_info.file
                break
        for ii in range(0, table[0].ext[i].dba_sum):
            if blk_sum >= table[0].blkcnt:
                break
            pos1 = (table[0].ext[i].dba_off_b + ii) * db1.page_size
            f.seek(pos1)  # 要判断返回值，是否成功
            data = f.read(db1.page_size)
            data1 = data[0:db1.page_size]
            page1 = page.record2(db1, data1, table, file_infos)  # 解析页面记录.  ***************
            tab_data.append(page1)
            blk_sum += 1
    return tab_data


# 初始化bootstrap$表
def init_bootstrap(file_infos):
    if file_infos[0].f_no == 1:
        pgfirst = file_infos[0].boot
    else:
        return
    init_sys_tab(file_infos[0])  # 初始化 db1
    ext, ext_sum, blk_sum = seg_unload(file_infos, 1, pgfirst)
    db1.tab0[0].file_no = 1
    db1.tab0[0].page_no = pgfirst
    db1.tab0[0].ext = ext
    db1.tab0[0].extcnt = ext_sum
    db1.tab0[0].blkcnt = blk_sum
    tab_data_bootstrap = page_unload_1(file_infos, db1.tab0[0])
    return tab_data_bootstrap, db1


# 初始化obj$ , C_OBJ#簇表, C_USER#簇表
def init_obj(file_infos, tab_data_bootstrap):
    for i in range(0, len(tab_data_bootstrap)):
        loop1 = tab_data_bootstrap[i].rec_sum
        for ii in range(0, loop1):
            if tab_data_bootstrap[i].record[ii].col_data2[1] == 18:  # obj$ 表,一般表. 慢
                len1 = len(tab_data_bootstrap[i].record[ii].col_data2[2])
                pgfirst_18 = tab_data_bootstrap[i].record[ii].col_data2[2][len1 - 5:len1 - 2]
                db1.tab0[1].file_no = 1
                db1.tab0[1].page_no = int(pgfirst_18)
                ext, ext_sum, blk_sum = seg_unload(file_infos, db1.tab0[1].file_no, db1.tab0[1].page_no)
                db1.tab0[1].ext = ext
                db1.tab0[1].extcnt = ext_sum
                db1.tab0[1].blkcnt = blk_sum
                tab_data_18 = page_unload_1(file_infos, db1.tab0[1])
            elif tab_data_bootstrap[i].record[ii].col_data2[1] == 2:  # C_OBJ# 表
                len1 = len(tab_data_bootstrap[i].record[ii].col_data2[2])
                pgfirst_2 = tab_data_bootstrap[i].record[ii].col_data2[2][len1 - 14:len1 - 11]
                db1.tab1[0].file_no = 1
                db1.tab1[0].page_no = int(pgfirst_2)
                ext, ext_sum, blk_sum = seg_unload(file_infos, db1.tab1[0].file_no, db1.tab1[0].page_no)
                db1.tab1[0].ext = ext
                db1.tab1[0].extcnt = ext_sum
                db1.tab1[0].blkcnt = blk_sum
                tab_data_2 = page_unload_2(file_infos, db1.tab1)
            elif tab_data_bootstrap[i].record[ii].col_data2[1] == 10:  # C_USER# 表
                len1 = len(tab_data_bootstrap[i].record[ii].col_data2[2])
                pgfirst_10 = tab_data_bootstrap[i].record[ii].col_data2[2][len1 - 14:len1 - 11]
                db1.tab2[0].file_no = 1
                db1.tab2[0].page_no = int(pgfirst_10)
                ext, ext_sum, blk_sum = seg_unload(file_infos, db1.tab2[0].file_no, db1.tab2[0].page_no)
                db1.tab2[0].ext = ext
                db1.tab2[0].extcnt = ext_sum
                db1.tab2[0].blkcnt = blk_sum
                tab_data_10 = page_unload_2(file_infos, db1.tab2)
    return tab_data_18, tab_data_2, tab_data_10


# 通过 C_OBJ# 初始化系统表,获得 tab$,icol$,col$,user$,ind$,lob$
def sys_tab_info(tab_data_2, tab_data_10):
    table_4 = [];
    table_21 = [];
    table_22 = [];
    table_19 = [];
    table_80 = [];
    table_20 = []
    for i in range(0, len(tab_data_2)):  # C_OBJ#
        for ii in range(0, len(tab_data_2[i].record)):
            if tab_data_2[i].record[ii].tab_no == 1:  # tab$ /4
                table_4.append(tab_data_2[i].record[ii])
            elif tab_data_2[i].record[ii].tab_no == 5:  # col$ /21
                table_21.append(tab_data_2[i].record[ii])
            elif tab_data_2[i].record[ii].tab_no == 3:  # ind$ /19
                table_19.append(tab_data_2[i].record[ii])
            elif tab_data_2[i].record[ii].tab_no == 4:  # icol$ /20
                table_20.append(tab_data_2[i].record[ii])
            elif tab_data_2[i].record[ii].tab_no == 6:  # lob$ /80
                table_80.append(tab_data_2[i].record[ii])
    for i in range(0, len(tab_data_10)):  # C_USER#
        for ii in range(0, len(tab_data_10[i].record)):
            if tab_data_10[i].record[ii].tab_no == 1:  # user$ /22
                table_22.append(tab_data_10[i].record[ii])
    table_22.sort(key=lambda x: (x.col_data2[1]))  # 按用户名排序 。支持多关键字排序

    return table_4, table_20, table_21, table_22, table_19, table_80  # tab$,icol$,col$,user$,ind$,lob$


# 初始化 所有表 的表结构
def tab_info(file_infos, tab_data_18, table_4, table_20, table_21, table_22, table_19, table_80):  # 很慢,循环方式可能有问题。循环层太多
    tables = [];
    indexes = []
    tab_data_18_sum = 0;
    tab_data_4_sum = len(table_4);
    tab_data_21_sum = len(table_21);
    for i in range(len(tab_data_18)):  # obj$
        tab_data_18_sum += len(tab_data_18[i].record)
    type = {1: 'varchar2', 2: 'number', 8: 'long', 12: 'date', 23: 'raw', 69: 'rowid', 96: 'char', 112: 'clob',
            113: 'blob', 114: 'bfile', 180: 'timestamp', 100: 'binary_float', 101: 'binary_double', 123: ''}  # 临时的处理办法
    for user in table_22:  # 用户
        if user.col_data2[0] >= 0 and user.col_data2[1] not in (
        'SYS', 'APEX_030200', 'MDSYS', 'OLAPSYS', 'SYSMAN', 'SYSTEM', 'XS$NULL', 'XDB', 'EXFSYS', 'CTXSYS', 'DBSNMP',
        'ORDDATA', 'WMSYS') and user.col_data2[2] == 1:
            #   if user.col_data2[0] != -87  and user.col_data2[2] == 1 :    # ********************* in(-1,83) 83：SCOTT
            print('user_id:%d,user_name:%s' % (user.col_data2[0], user.col_data2[1]))
            for i in range(len(tab_data_18)):  # obj$
                for ii in range(len(tab_data_18[i].record)):
                    if tab_data_18[i].record[ii].col_data2[6] == 2 and tab_data_18[i].record[ii].col_data2[2] == \
                            user.col_data2[0]:  # table
                        # col_data2[6]对象类型：19是分区表,1是index,2是table. col_data2[2]是 所有者用户ID.
                        # print('tab_name: %s.%s,sub_tab_name:%s,tab_obj_id:%d,data_obj_id:%s'%(user.col_data2[1],tab_data_18[i].record[ii].col_data2[3],\
                        # tab_data_18[i].record[ii].col_data2[5],tab_data_18[i].record[ii].col_data2[0],tab_data_18[i].record[ii].col_data2[1]))
                        # continue
                        for iii in range(len(table_4)):  # tab$
                            if (tab_data_18[i].record[ii].col_data2[0] == table_4[iii].col_data2[0]) and \
                                    table_4[iii].col_data2[1] not in (2, 10):
                                # or tab_data_18[i].record[ii].col_data2[0] == table_4[iii].col_data2[5]
                                table1 = table_struct.st_table()
                                table1.tab_name = tab_data_18[i].record[ii].col_data2[3]
                                table1.tab_obj_id = table_4[iii].col_data2[0]
                                table1.ts = table_4[iii].col_data2[2]
                                table1.owner = tab_data_18[i].record[ii].col_data2[2]
                                table1.owner_name = user.col_data2[1]
                                table1.file_no = table_4[iii].col_data2[3]
                                table1.page_no = table_4[iii].col_data2[4]
                                table1.rowcnt = table_4[iii].col_data2[15]
                                table1.col_sum = table_4[iii].col_data2[7]
                                #    print('表 %s.%s 的段头页: %d/%d'%(user.col_data2[1],table1.tab_name,table1.file_no,table1.page_no))
                                ext, ext_sum, blk_sum = seg_unload(file_infos, table1.file_no, table1.page_no)
                                table1.ext = ext
                                table1.extcnt = ext_sum
                                table1.blkcnt = blk_sum
                                for i1 in range(len(table_21)):  # col$
                                    if table_21[i1].col_data2[0] == table1.tab_obj_id:
                                        column1 = table_struct.st_column()
                                        column1.tab_obj_id = table_21[i1].col_data2[0]
                                        column1.col_id = table_21[i1].col_data2[1]
                                        column1.col_name = table_21[i1].col_data2[5]
                                        column1.col_type = table_21[i1].col_data2[6]
                                        column1.col_len = table_21[i1].col_data2[7]
                                        if column1.col_type in (1, 96, 23):
                                            column1.col_type_name = type[column1.col_type] + '(%s)' % column1.col_len
                                        else:
                                            try:
                                                column1.col_type_name = type[column1.col_type]
                                            except KeyError:
                                                column1.col_type_name = 'unkown'
                                        table1.col.append(column1)
                                tables.append(table1)
                                break
                    elif tab_data_18[i].record[ii].col_data2[6] == 1 and tab_data_18[i].record[ii].col_data2[2] == \
                            user.col_data2[0]:  # index
                        for iii in range(len(table_19)):  # ind$
                            if (tab_data_18[i].record[ii].col_data2[0] == table_19[iii].col_data2[1]):
                                # print('************obj_name: %s.%s,obj_subname:%s,obj_id:%d,data_obj_id:%s'%(user.col_data2[1],tab_data_18[i].record[ii].col_data2[3],\
                                # tab_data_18[i].record[ii].col_data2[5],tab_data_18[i].record[ii].col_data2[0],tab_data_18[i].record[ii].col_data2[1]))
                                index1 = table_struct.st_index()
                                index1.obj_id = table_19[iii].col_data2[1]
                                index1.bobj = table_19[iii].col_data2[0]
                                index1.ind_name = tab_data_18[i].record[ii].col_data2[3]
                                index1.col_sum = table_19[iii].col_data2[7]
                                index1.ts = table_19[iii].col_data2[3]
                                index1.file_no = table_19[iii].col_data2[4]
                                index1.page_no = table_19[iii].col_data2[5]
                                for i1 in range(len(table_20)):  # icol$
                                    if table_20[i1].col_data2[1] == index1.obj_id:
                                        column1 = table_struct.st_column()
                                        column1.tab_obj_id = table_20[i1].col_data2[0]
                                        column1.col_id = table_20[i1].col_data2[2]
                                        column1.pos = table_20[i1].col_data2[3]
                                        index1.col.append(column1)
                                indexes.append(index1)
                                #     print(index1.ind_name,index1.file_no,index1.page_no)
                                break
                    elif tab_data_18[i].record[ii].col_data2[6] == 21 and tab_data_18[i].record[ii].col_data2[2] == \
                            user.col_data2[0]:  # lob
                        for iii in range(len(table_80)):  # lob$ ,   好像没啥用
                            if (tab_data_18[i].record[ii].col_data2[0] == table_80[iii].col_data2[3]):
                                # print('****lob****obj_name: %s.%s,obj_subname:%s,obj_id:%d,data_obj_id:%s'%(user.col_data2[1],tab_data_18[i].record[ii].col_data2[3],\
                                # tab_data_18[i].record[ii].col_data2[5],tab_data_18[i].record[ii].col_data2[0],tab_data_18[i].record[ii].col_data2[1]))
                                tab_obj_id = table_80[iii].col_data2[0]
                                lobj_id = table_80[iii].col_data2[3]
                                col_id = table_80[iii].col_data2[1]
                                ind_id = table_80[iii].col_data2[5]
                                ts = table_80[iii].col_data2[6]
                                file_no = table_80[iii].col_data2[7]
                                page_no = table_80[iii].col_data2[8]
                        #     print('lob 的段头页: %d/%d,,%d,%d,%d,%d'%(file_no,page_no,tab_obj_id,lobj_id,col_id,ind_id))

                    elif tab_data_18[i].record[ii].col_data2[6] in (7, 8, 9) and tab_data_18[i].record[ii].col_data2[
                        2] == user.col_data2[0]:  # 包，函数
                        a = 0
                        # print('==函数=====obj_name: %s.%s,obj_subname:%s,obj_id:%d,data_obj_id:%s'%(user.col_data2[1],tab_data_18[i].record[ii].col_data2[3],\
                        # tab_data_18[i].record[ii].col_data2[5],tab_data_18[i].record[ii].col_data2[0],tab_data_18[i].record[ii].col_data2[1]))

    # 分区表，分区索引， 函数
    # 把索引关联到表里。  解大lob数据走索引。

    tables.sort(key=lambda x: (x.tab_name))  # 排序 。支持多关键字排序

    for table in tables:  # 表的索引
        for index in indexes:
            if table.tab_obj_id == index.bobj:
                for i in range(len(index.col)):
                    try:
                        index.col[i] = table.col[index.col[i].col_id - 1]
                    except IndexError:
                        continue
                    index.col[i].col_id = i
                table.indexes.append(index)
    print(tab_data_18_sum, tab_data_4_sum, tab_data_21_sum)
    #  obj$, tab$, col$
    #  74680 3434  103450
    #  74787 3446  103661
    return tables


# 解析所有表
def unload_all(file_infos, tables, db):
    table_data = []
    for i in range(0, len(tables)):  # 解析每个表
        table_data1 = page_unload_1(file_infos, tables[i])
        table_data.append(table_data1)  # 解析表数据
    #  save_all(tables[i],table_data,db)      #  把表数据存储在db中
    return table_data


# 解析一个表
def unload_tab(file_infos, table, db):
    table_data1 = page_unload_1(file_infos, table)  # 解析表数据
    #  save_all(tables[i],table_data,db)      #  把表数据存储在db中
    return table_data1


def tab_sql(table1):
    ss = 'CREARE TABLE ' + '\"%s\".\"%s\"' % (table1.owner_name, table1.tab_name) + ' ('
    # for i2 in range(0,table1.col_sum):        # 挪出此函数
    #     if i2 == table1.col_sum-1 :  #　　建表语句
    #         try:
    #             ss += '%s %s'%(table1.col[i2].col_name,table1.col[i2].col_type_name) + ');'
    #         except IndexError:
    #             continue
    #     else:
    #         try:
    #             ss += '%s %s'%(table1.col[i2].col_name,table1.col[i2].col_type_name) +  ','
    #         except IndexError:
    #             continue
    table1.sql = ss


# 把表数据存储在sqlite中
def save_all(table, table_data, db):  # 把表数据存储在db中
    conn = sqlite3.connect(db)  # 打开数据库
    cursor = conn.cursor()
    print(table.sql)
    cursor.execute(table.sql)  # 创建解析的表，然后把解析的数据存储进去
    for i in range(0, len(table_data)):  # 每一页
        for i1 in range(0, table_data[i].rec_sum):
            ss = ''
            for i2 in range(0, table.col_sum):
                if i2 == table.col_sum - 1:
                    ss += '\'' + str(table_data[i].record[i1].col_data1[i2]) + '\''
                else:
                    ss += '\'' + str(table_data[i].record[i1].col_data1[i2]) + '\'' + ','
            print(ss)
            cursor.execute("insert into %s values( %s );" % (table.tab_name, ss))  # 插入数据
        conn.commit()
    cursor.close()
