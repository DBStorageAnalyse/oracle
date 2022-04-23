# -*- coding: utf-8 -*-
# sql server 碎片物理拼接 连续性拼接,半页聚合. 需要读源数据和sqlite库。
import sqlite3, struct, time
import ctl_check


def link_1(db_name):
    print("\nbegin link_1 ...  \nDatetime: " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                             time.localtime(time.time())))  # current time
    conn1 = sqlite3.connect(db_name)
    cursor1 = conn1.cursor()
    cursor1.execute("select offset,page_no,file_no from ora_page ")  # 其实是按offset排序的
    page_size = 16384
    v_2 = []
    print('开始 进入内存,稍等 ... ')
    v_1 = cursor1.fetchall()  # 取出数据, 里边的成员不能修改
    if len(v_1) == 0:
        print('没有碎片,link_1完成 ... ')
        return
    v_1.append(v_1[0])
    cursor1.close()
    conn1.close()
    print('已经进入内存,开始拼接... ')
    for i in range(len(v_1) - 1):  # 开始拼接物理碎片。 太多了，注意性能
        if i % 10000 == 0 or i == len(v_1) - 2:
            print("拼接： Percent:%d%% \r" % (i / (len(v_1) - 2) * 100), end="")
        if i == 0:
            aa_2 = ctl_check.values2()
            v_2.append(aa_2)
            del aa_2

        #   拼碎片
        a = (v_1[i + 1][0] - v_1[i][0]) / page_size == (v_1[i + 1][1] - v_1[i][1]) and (
                    v_1[i + 1][1] - v_1[i][1]) > 0 and (v_1[i + 1][1] - v_1[i][1]) <= 8
        # v_1[i][2] == v_1[i+1][2] and    文件号相同

        if a == 1:
            if v_2[-1].page_sum == 1:
                v_2[-1].offset_1 = v_1[i][0]
                v_2[-1].page_no_1 = v_1[i][1]
                v_2[-1].file_no_1 = v_1[i][2]
                if v_2[-1].file_no_1 == 1023 or v_2[-1].file_no_1 == 0:
                    v_2[-1].file_no_1 = v_1[i + 1][2]
                v_2[-1].page_sum = 2
        if a == 0:
            v_2[-1].offset_2 = v_1[i][0]
            v_2[-1].page_no_2 = v_1[i][1]
            v_2[-1].file_no_2 = v_1[i][2]
            v_2[-1].page_sum = v_2[-1].page_no_2 - v_2[-1].page_no_1 + 1
            aa_2 = ctl_check.values2()  # 下一个碎片开始
            aa_2.file_no_1 = v_1[i + 1][2]
            aa_2.offset_1 = v_1[i + 1][0]
            aa_2.page_no_1 = v_1[i + 1][1]
            aa_2.offset_2 = v_1[i + 1][0]
            aa_2.page_no_2 = v_1[i + 1][1]
            aa_2.file_no_2 = v_1[i + 1][2]
            aa_2.page_sum = 1
            if i != len(v_1) - 2:
                v_2.append(aa_2)
            del aa_2
    del v_1
    # link_1记录片段信息：片段号，片段中页数，起始页信息(物理偏移，页号，文件号)，结束页信息(物理偏移，页号，文件号)
    # print("\nbegin insert link_1 ...")
    db2 = db_name
    conn2 = sqlite3.connect(db2)
    cursor2 = conn2.cursor()
    cursor2.execute(
        "create table link_1(id integer primary key,offset_1,offset_2,page_sum,page_no_1,page_no_2,file_no_1,g1_id,g1in_id,s_pos,e_pos)")

    for i in range(len(v_2)):
        if v_2[i].file_no_1 == 1023 or v_2[i].file_no_1 == 0:  # 碎片的起始文件号不正常时记结尾文件号
            v_2[i].file_no_1 == v_2[i].file_no_2
        cursor2.execute(
            "insert into link_1(offset_1,offset_2,page_sum,page_no_1,page_no_2,file_no_1) values(?,?,?,?,?,?)", \
            (v_2[i].offset_1, v_2[i].offset_2, v_2[i].page_sum, v_2[i].page_no_1, v_2[i].page_no_2, v_2[i].file_no_1))
        if i % 100000 == 0 or i == len(v_2) - 1:
            #     print("insert： Percent:%d%% \r"%(i/((len(v_2)-1)*100+1)),end="")
            conn2.commit()
    cursor2.close()
    conn2.commit()
    conn2.close()
    del v_2
    print("\nDatetime: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # current time


def link_wl(f_name, db_name):  # 物理拼接汇总
    link_1(db_name)  # 物理连续拼接
    print("物理拼接完成...")

# f_name = r'F:\ruyang.img'
# db_name = r'E:\ora_scan_1.db'
# link_wl(f_name,db_name)
