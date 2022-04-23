# -*- coding: utf-8 -*-
# 解析 指定的表数据
import struct, os.path, sqlite3, time  # cx_Oracle
import page, table_struct

s = struct.unpack  # B,H,I


class Unload_Obj():
    def __init__(self):  # 解析函数
        super(Unload_Obj, self).__init__()
        self.db1 = 0
        self.oracle = 0

    def init_db(self):  # 初始化 db1
        self.db1 = table_struct.st_db()
        self.db1.endian = '>'
        self.db1.page_size = 16384
        self.db1.version = '11.2'
        #   self.oracle = cx_Oracle.connect('scott','tiger','192.168.1.107/orcl')  # 建立连接，3 个参数分开写
        db = './unload_tab.db'  # 数据库文件名称
        # create table tab_info(id integer primary key,tab_obj_id,BOBJ,TAB_NO,user_name,tab_name,col_sum)
        conn = sqlite3.connect(db)  # 打开数据库
        cursor = conn.cursor()
        cursor.execute("select * from tab_info order by tab_obj_id ")
        values_tab = cursor.fetchall()  # 返回数据为二维数组
        print('init db...')
        for i in range(len(values_tab)):  # 初始化表结构
            table1 = table_struct.st_table()
            table1.tab_obj_id = int(values_tab[i][1])
            table1.bobj = values_tab[i][2]
            table1.tab_no = values_tab[i][3]
            table1.owner_name = values_tab[i][4]
            table1.tab_name = values_tab[i][5]
            table1.col_sum = values_tab[i][6]
            cursor.execute(
                "select c.* from tab_info t,col_info c where c.tab_obj_id = t.bobj and t.tab_obj_id='%s' order by c.col_id " % (
                    table1.tab_obj_id))  #
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
            self.db1.tab0.append(table1)
        cursor.close()
        conn.close()
        print('init db over...')

    # 解析 普通表
    def unload_all(self, file):
        f = open(file, 'rb')
        f_size = os.path.getsize(file)
        buf = 8  # buffer ,不是太重要
        buffer = int(1024 * 1024 * buf)  # 32M
        loop_1 = f_size // buffer
        loop_2 = buffer // self.db1.page_size
        size_1 = f_size % buffer
        begin = time.time()
        print("Datetime: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin)))  # current time
        fmt = {512: 0x22, 1024: 0x42, 2048: 0x62, 4096: 0x82, 8192: 0xa2, 16384: 0xc2, 32768: 0xe2}
        page_sum = 0;
        recode_sum = 0;
        page_size = self.db1.page_size;
        fmt_1 = fmt[page_size]
        for i in range(loop_1 + 1):
            f.seek(buffer * i)
            data = f.read(buffer)
            if i == loop_1:
                loop_2 = size_1 // page_size
            for ii in range(loop_2):  # 每个页面
                data_0 = data[page_size * ii:page_size * (ii + 1)]
                data_1 = s('2B', data_0[0:2])
                if data_1[0] == 6 and data_1[1] == fmt_1:
                    data_2 = s(self.db1.endian + 'BBHI', data_0[20:28])
                    if data_2[0] == 1:
                        obj_id = data_2[3]
                        mid = self.BinarySearch(self.db1.tab0, obj_id)
                        if mid != -1:  #
                            page_data = page.record1(self.db1, data_0, self.db1.tab0[mid])
                            for record in page_data.record:
                                self.db1.tab0[mid].ext.append(record.col_data2)  # 解析的表数据
                            page_sum += 1;
                            recode_sum += len(page_data.record)
                            if len(self.db1.tab0[mid].ext) > 5000:
                                self.out_2(self.db1.tab0[mid])  # 插入到 oracle
                                self.db1.tab0[mid].ext = []
                # if ii%100 == 0:
                #     print('read:%sM, page:%d, recode:%d \r'%((i+1)*buf,page_sum,recode_sum),end='')
            end = time.time()
            print("\nread:%sM, I/O:%.2f M/s, I/O:%d recode/s" % (
            (i + 1) * buf, (i + 1) * buf / (end - begin + 1), int(recode_sum / (end - begin + 1))))  # I/O

    def BinarySearch(self, a, target):  # 二分查找，a 是被查找的排好序的数组，target是要查的条目
        low = 0
        high = len(a) - 1
        while low <= high:
            mid = (low + high) // 2
            midVal = a[mid]
            if midVal.tab_obj_id < target:
                low = mid + 1
            elif midVal.tab_obj_id > target:
                high = mid - 1
            else:
                return mid
        return -1

    # 导出到oracle库中
    def out_1(self, tab):
        cursor = self.oracle.cursor()
        s1 = '';
        s2 = ''
        for ii in range(tab.col_sum):
            if ii == tab.col_sum - 1:  # 建表语句
                try:
                    s1 += tab.col[ii].col_name
                    s2 += ':%d' % (ii + 1)
                except IndexError:
                    continue
            else:
                try:
                    s1 += tab.col[ii].col_name + ','
                    s2 += ':%d' % (ii + 1) + ','
                except IndexError:
                    continue
        cursor.prepare("INSERT INTO %s.%s(%s) VALUES (%s)" % (tab.owner_name, tab.tab_name, s1, s2))
        cursor.executemany(None, tab.ext)
        cursor.close()
        self.oracle.commit()

    # 导出为 txt
    def out_2(self, tab):
        f1 = open(r'.\%s.txt' % tab.tab_name, 'a')
        s = ''
        for ss in tab.ext:
            for i in range(len(ss)):
                if i == len(ss) - 1:
                    s += str(ss[i]) + '\n'
                else:
                    s += str(ss[i]) + '|'
        f1.writelines(s)
        f1.close()


def unload(file):
    unload_tab = Unload_Obj()
    unload_tab.init_db()
    unload_tab.unload_all(file)
    print('over...')


file = r'D:\data\tbs_dat_cdr_043.dbf'
unload(file)
