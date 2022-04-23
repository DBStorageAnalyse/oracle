#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 读取数据库文件进行解析, 主函数 模块
from PyQt5.QtCore import QThread, pyqtSignal
import struct, time, sqlite3
import init

s = struct.unpack


class Unload_DB(QThread):
    PUP = pyqtSignal(int)  # 更新进度条的信号
    LUP = pyqtSignal(str)

    def __init__(self, parent=None):  # 解析函数
        super(Unload_DB, self).__init__(parent)
        self.file_infos = []
        self.tables = 0
        self.table_22 = 0
        self.db1 = 0

    # 文件信息
    def file_init(self, fn):
        self.file_infos = []
        for f_name in fn:  # 每个文件头信息
            f = open(f_name, 'rb')
            data = f.read(32)
            file_info = init.file_blk_0(data)
            if file_info.blk_size not in (512, 1024, 2048, 4096, 8192, 16384, 32768):
                file_info.f_name = f_name
                file_info.file = f
                self.file_infos.append(file_info)
                continue
            f.seek(file_info.blk_size)
            data = f.read(file_info.blk_size)
            file_info = init.file_blk_1(data)
            file_info.f_name = f_name
            file_info.file = f
            self.file_infos.append(file_info)
        return self.file_infos

    def run(self):
        self.unload_db(self.file_infos)

    # 正常解析system.dbf文件
    def unload_db(self, file_infos):
        print("Datetime: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        tab_data_bootstrap, db1 = init.init_bootstrap(file_infos)  # 解析bootstrap$表
        self.PUP.emit(10)  # 传递参数
        self.LUP.emit("\t初始化 obj$表,C_OBJ#簇表 ...")
        tab_data_18, tab_data_2, tab_data_10 = init.init_obj(file_infos,
                                                             tab_data_bootstrap)  # 解析obj$表,C_OBJ#簇表,C_USER#簇表  慢 ...
        self.PUP.emit(20)  # 传递参数
        self.LUP.emit("\t初始化 系统表 ...")
        table_4, table_20, table_21, table_22, table_19, table_80 = init.sys_tab_info(tab_data_2,
                                                                                      tab_data_10)  # 通过 C_OBJ#,C_USER# 初始化系统表,获得tab$,col$,user$
        print("初始化 系统表 over ...\n")
        self.PUP.emit(50)  # 传递参数
        self.LUP.emit("\t初始化 普通表 ...")
        tables = init.tab_info(file_infos, tab_data_18, table_4, table_20, table_21, table_22, table_19,
                               table_80)  # 初始化所有的表结构
        print("初始化 普通表 over ...\n")
        self.PUP.emit(100)
        self.LUP.emit("\t解析 over ...")
        # table_data = init.unload_all(file_infos,tables,'')                                  # 解析所有表数据
        self.tables, self.table_22, self.db1 = tables, table_22, db1

    # 获取表结构到sqlite
    def tab_info(self, tab, db):
        print('开始 获取表结构到sqlite ...')
        db = './db_1.db';
        f = open(db, 'w');
        f.close()
        conn = sqlite3.connect(db);
        cursor = conn.cursor()
        cursor.execute(
            "create table tab_info(id integer primary key,tab_name,sub_tab_name,tab_type,tab_obj_id,data_obj_id,col_sum)")
        cursor.execute("create table col_info(id integer primary key,tab_obj_id,col_id,col_name,col_data_type,col_len)")

        #      sql = "insert into tab_info(tab_name,sub_tab_name,tab_type,tab_obj_id,data_obj_id,col_sum) values('%s','%s',%d,%d,%s,%d);"%\
        #                          (tab_data_18[i].record[ii].col_data2[3],tab_data_18[i].record[ii].col_data2[5],tab_data_18[i].record[ii].col_data2[6],\
        #                          tab_data_18[i].record[ii].col_data2[0],tab_data_18[i].record[ii].col_data2[1],table1.col_sum)

        for table in tab:
            cursor.execute(
                "insert into tab_info(tab_name,sub_tab_name,tab_type,tab_obj_id,data_obj_id,col_sum) values('%s','%s',%d,%d,%s,%d);" % \
                (table.db_name, table.tab_name, 0, table.tab_obj_id, table.index_id, table.col_sum))
            for col in table.col:
                if col.tab_obj_id == table.tab_obj_id:
                    cursor.execute(
                        "insert into col_info(tab_obj_id,col_id,col_name,col_data_type,col_len) values(%d,%d,%s,%d,%d)" % \
                        (col.tab_obj_id, col.col_id, '\'' + col.col_name + '\'', col.col_type, col.col_len))
            conn.commit()
        conn.commit()
        print('获取表结构到sqlite 完成...')

    # 正常解析表,解一个表
    def unload_tab(self, file_infos, table, db):
        table_data = init.unload_tab(file_infos, table, db)
        return table_data

# db = r'C:\Users\zsz\PycharmProjects\oracle\test\system01.db'        # 数据输出的数据库文件名称
# f_name = r'C:\Users\zsz\PycharmProjects\oracle\ora_unload\system01.dbf'     #
# unload_dbf_test(f_name,db)
