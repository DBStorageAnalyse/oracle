# -*- coding: utf-8 -*-
# oracle 表结构信息获取。 适用 navacate,toad,exp 导出的sql
# 从建表sql 中获取数据库信息，写出到ini或数据库

import re, sqlite3
import configparser  # 处理配置文件


class Column:
    def __init__(self):
        self.column_name = ''  # 列名
        self.column_data_type = 0  # 数据类型
        self.column_data_base1 = ''  # 括号数1
        self.column_data_base2 = ''  # 括号数2
        self.column_length = 0  # 数据长度
        self.column_var_is = 1  # 是否是边长
        self.column_define = ''  # 默认值
        self.column_pkey_is = 0  # 列是否是主键，1是0否
        self.column_nullable_is = 1  # 是否可以为空，1是 0不可为空
    # self.enums = list() # enum 类型


# table 结构体
class Table:
    def __init__(self, num, schema, name):
        self.num = num  # 表编号，从1开始
        self.schema = schema
        self.table_name = name
        self.table_type = 1  # 暂时只有这一个选项，可扩充
        self.columns = []

    @property
    def column_sum(self):
        return len(self.columns)

    # @property
    # def nullmap_is(self):
    #     nullable = False
    #     for column in self.columns:
    #         nullable = nullable or (column.column_nullable_is == 1)
    #     return int(nullable)


# 列数据长度
def parse_len(type_name, column_stmt):
    type_len = {'VARCHAR2': 0, 'NVARCHAR2': 0, 'CHAR': 0, 'NCHAR': 0, 'DATE': 7, 'NUMBER': 0, 'INTEGER': 0, 'FLOAT': 0,
                'TIMESTAMP': 8}
    if type_name in type_len:
        if type_name == 'VARCHAR2':
            try:
                len1 = int(re.search(r'\((\d+) BYTE\)', column_stmt).group(1))  # ***** 【调整】
            except AttributeError:
                len1 = 0
            return len1
        return type_len[type_name]
    else:
        return 0


# 从create语句中提取 列信息
def parse_create_stmt(create_stmt):
    #  iter = re.finditer(r'\n (\w+) (\w+)*', create_stmt)    # ******** 【调整】
    iter = re.finditer(r'\n (\w+) (\w+).*', create_stmt)  # *****toad
    columns = []
    type = {'VARCHAR2': 1, 'NVARCHAR2': 0, 'CHAR': 96, 'NCHAR': 95, 'DATE': 12, 'NUMBER': 2, 'INTEGER': 2,
            'TIMESTAMP': 180, \
            'LONG': 8, 'CLOB': 112, 'BLOB': 113, 'FLOAT': 2}
    for m in iter:  # 每一行
        column = Column()
        column.column_name = m.group(1)
        column.column_data_type = type[m.group(2)]
        column.column_length = parse_len(m.group(2), m.group())
        columns.append(column)
        #  print(m.group()[-1:])
        if m.group()[-1:] != ',':
            return columns
    return columns


# 将table信息写入配置文件
def save_table1(table):
    print("%s.%s" % (table.schema, table.table_name))
    conf = configparser.ConfigParser()
    # 写入数据库信息
    conf.add_section('database')
    conf.set('database', 'db_type', '30')
    # 写入表信息
    conf.add_section('table')
    conf.set('table', 'table_name', table.table_name)
    conf.set('table', 'table_type', str(table.table_type))  # 'table_%d' % table.num,
    conf.set('table', 'column_sum', str(table.column_sum))

    # 写入列信息
    column_num = 0
    for column in table.columns:
        conf.add_section('column_%d' % column_num)
        conf.set('column_%d' % column_num, 'column_name', column.column_name)
        conf.set('column_%d' % column_num, 'column_data_type', column.column_data_type)
        if column.column_data_type == 'numeric' or column.column_data_type == 'decimal':
            conf.set('column_%d' % column_num, 'column_data_base1', column.column_data_base1)
            conf.set('column_%d' % column_num, 'column_decimal_xlen', column.column_data_base2)  # column_data_base2
        elif column.column_data_type == 'money':
            conf.set('column_%d' % column_num, 'column_data_base1', '19')
            conf.set('column_%d' % column_num, 'column_decimal_xlen', '4')

        conf.set('column_%d' % column_num, 'column_length', str(column.column_length))
        # conf.set('column_%d' % column_num, 'column_var_is', str(column.column_var_is))
        # conf.set('column_%d' % column_num, 'column_define', '0')
        # conf.set('column_%d' % column_num, 'column_pkey_is', '0')
        # conf.set('column_%d' % column_num, 'column_nullable_is', str(column.column_nullable_is))
        column_num += 1
    conf.write(open('./12/%s.ini' % (table.table_name), 'w'))


# 将table信息写入sqlite的表中
def save_table2(table, conn):
    print("%s.%s" % (table.schema, table.table_name))
    cursor = conn.cursor()
    cursor.execute("insert into tab_info(tab_obj_id,tab_type,tab_name,col_sum) values(%d,%d,%s,%d)" % (
    table.num, 0, '\'' + table.table_name + '\'', table.column_sum))
    for i in range(0, table.column_sum):
        a = 0
        cursor.execute(
            "insert into col_info(tab_obj_id,col_id,col_name,col_data_type,col_len) values(%d,%d,%s,%d,%d)" % (
            table.num, i + 1, '\'' + table.columns[i].column_name + '\'', table.columns[i].column_data_type,
            table.columns[i].column_length))
    conn.commit()


# 将table信息写入sqlldr 控制文件
def save_table3(table, path):
    f1 = open(path + '\\' + table.table_name + '.ctl', 'w')  # 打开sql文件
    f1.write(
        "OPTIONS(BINDSIZE=20480000,READSIZE=20480000,ERRORS=1000000,ROWS=50000)\nLOAD DATA\nINFILE '%s.txt' \"STR X'0d0a'\"\nAPPEND INTO TABLE \"%s\".\"%s\"\nFIELDS TERMINATED BY '|'\nTRAILING NULLCOLS \n(\n" % (
        table.table_name, table.schema, table.table_name))
    len_1 = len(table.columns)
    for i in range(len_1):
        if i < len_1 - 1:
            if table.columns[i].column_data_type == 12:
                f1.write('"%s" DATE "YYYY-MM-DD HH24:MI:SS",\n' % table.columns[i].column_name.upper())
            elif table.columns[i].column_data_type == 1 and table.columns[i].column_length > 255:
                f1.write('"%s" CHAR(%d),\n' % (table.columns[i].column_name.upper(), table.columns[i].column_length))
            else:
                f1.write('"%s",\n' % table.columns[i].column_name.upper())
        elif i == len_1 - 1:
            if table.columns[i].column_data_type == 12:
                f1.write('"%s" DATE "YYYY-MM-DD HH24:MI:SS"\n' % table.columns[i].column_name.upper())
            elif table.columns[i].column_data_type == 1 and table.columns[i].column_length > 255:
                f1.write('"%s" CHAR(%d)\n' % (table.columns[i].column_name.upper(), table.columns[i].column_length))
            else:
                f1.write('"%s"\n' % table.columns[i].column_name.upper())
    f1.write(")\n")
    f1.close()


# 获取 create 脚本
def save_table4(table, create_stmt, f1):
    f1.write('CREATE TABLE %s.%s\n(' % (table.schema, table.table_name))
    iter = re.finditer(r'\n (\w+) (\w+).*', create_stmt)  # *****toad
    for m in iter:  # 每一行
        f1.write(m.group())  # f1.write
        if m.group()[-1:] != ',':
            f1.write('\n);\n\n')
            return 0


# 主函数， 选择性的导出表结构
def table_frm2(sql_file_name, db):
    f = open(sql_file_name, encoding='utf-8')  # 打开sql文件
    f1 = open(db, 'wb');
    f1.close()  # 创建sqlite数据库
    conn = sqlite3.connect(db)  # 打开sqlite数据库
    data = f.read()
    #   pattern_create_stmt = re.compile(r'CREATE TABLE \"(\w+)\"\.\"(\w+)\" \(\n(.+\n)*')  # 用于匹配oracle的标准create块  **** 【调整】
    pattern_create_stmt = re.compile(r'CREATE TABLE (\w+)\.(\w+)\n\(\n(.+\n)*')  # 用于匹配toad的create块  **** 【调整】
    iter = pattern_create_stmt.finditer(data)  # 在data 中查找'CREATE TABLE', 查找结果存储在iter中
    table_num = 1
    cursor = conn.cursor()
    cursor.execute(
        'create table tab_info(id integer primary key,tab_name,sub_tab_name,tab_type,tab_obj_id,data_obj_id,col_sum)')
    cursor.execute('create table col_info(id integer primary key,tab_obj_id,col_id,col_name,col_data_type,col_len)')
    cursor.execute('select * from aa')  # **** 【调整】
    values = cursor.fetchall()
    path = r'C:\Users\zsz\Desktop\qinghai_his\tables\sqlldr'
    f1 = open(r'C:\Users\zsz\Desktop\qinghai_his\tables\W_242.sql', 'w+')  # 打开sql文件
    for m in iter:
        for i in range(len(values)):
            if values[i][1].strip() == m.group(2):
                table_num = values[i][2]
                table = Table(table_num, m.group(1), m.group(2))  # 初始化table结构体
                #   table = Table(table_num, 'PORTAL_HIS', m.group(1))  # 初始化table结构体
                table.columns = parse_create_stmt(m.group())  # m.group()是一个create 语句. 从create语句中提取列信息
                save_table4(table, m.group(), f1)  # 将table信息写入sqlldr 控制文件
            #    save_table2(table,conn)                                 # 将table信息写入SQLite文件
            #    save_table1(table,conn)                                 # 将table信息写入ini文件
            #    save_table3(table,path)                                 # 将table信息写入sqlldr 控制文件

            #  table_num += 1
    conn.close()
    f.close()


# 主函数，全部的导出表结构
def table_frm1(sql_file_name, out_db):
    f = open(sql_file_name, encoding='utf-8')
    data = f.read()
    f1 = open(out_db, 'wb');
    f1.close()
    conn = sqlite3.connect(out_db)  # 打开数据库
    cursor = conn.cursor()
    cursor.execute(
        "create table tab_info(id integer primary key,db_name,tab_name,tab_type,tab_id,ind_id,ts_no,col_sum,nullable_sum,var_len_sum)")
    cursor.execute(
        "create table col_info(id integer primary key,tab_id,col_id,col_name,col_type,col_len,prec,scale,notnull_is,pkey_is,var_len_is,unsign_is)")
    pattern_create_stmt = re.compile(r'CREATE TABLE (\w+)\.(\w+)\n\(\n(.+\n)*')  # 用于匹配toad的create块  **** 【调整】
    iter = pattern_create_stmt.finditer(data)
    table_num = 1
    for m in iter:
        table = Table(table_num, m.group(1), m.group(2))
        table.col = parse_create_stmt(m.group())  # m.group() 一个create 语句
        save_table2(table, conn)
        print("table:%s" % (table.tab_name))
        table_num += 1


sql_name = r'C:\Users\zsz\Desktop\qinghai_his\tables\WWW.sql'
db_name = r'C:\Users\zsz\Desktop\qinghai_his\tables\his.db'  # 数据库文件名称
table_frm1(sql_name, db_name)
