#!/usr/bin/env python
# -*- coding: utf-8 -*-
# page ,  record, 大/小端
import struct
import table_struct

s = struct.unpack  # B,H,I


# 数据类型解析,需要完善
def data_type(data, col, file_infos):
    # 数字 number
    if col.col_type == 2:
        data_2_2 = 0;
        data_3_2 = 0
        data_0 = len(data)  # 数据的总长度
        if data_0 == 0:
            return ''  # 有待确认
        data_1 = s('B', data[0:1])  # data 直接就是数据， data_1是整数存储位数
        if data_1[0] > 0x80:  # 正数
            data_1_1 = data_1[0] - 0xC0  # 整数数据的长度
            data_3_0 = data_0 - data_1_1 - 1  # 小数数据的长度
            data_2 = data[1:data_1_1 + 1]  # 整数数据
            data_3 = data[data_1_1 + 1:data_0]  # 小数数据

            if data_3_0 >= 0:  # 有小数
                for i1 in range(0, data_1_1):  # 整数
                    data_2_1 = s('B', data_2[i1:i1 + 1])
                    data_2_2 += (data_2_1[0] - 1) * (100 ** (data_1_1 - i1 - 1))
                for i2 in range(0, data_3_0):  # 小数
                    data_3_1 = s('B', data_3[i2:i2 + 1])
                    data_3_2 += (data_3_1[0] - 1) * (0.01 ** (i2 + 1))
            if data_3_0 < 0:  # 200000  尾部的00不存
                data_2 = data[1:data_0]
                for i3 in range(0, data_0 - 1):  # 整数
                    data_2_1 = s('B', data_2[i3:i3 + 1])
                    data_2_2 += (data_2_1[0] - 1) * (100 ** (data_1_1 - i3 - 1))
            data_out = data_2_2 + data_3_2
        elif data_1[0] < 0x80:  # 负数
            data_1_1 = 0xff - data_1[0] - 0xc0  # 整数数据的长度
            data_3_0 = data_0 - data_1_1 - 2  # 小数数据的长度
            data_2 = data[1:data_1_1 + 1]  # 整数数据
            data_3 = data[data_1_1 + 1:data_0]  # 小数数据
            if data_3_0 >= 0:  # 有小数 如：-2011.33
                for i1 in range(0, data_1_1):  # 整数
                    data_2_1 = s('B', data_2[i1:i1 + 1])
                    data_2_3 = 0x66 - data_2_1[0] - 1
                    data_2_2 += data_2_3 * (100 ** (data_1_1 - i1 - 1))
                for i2 in range(0, data_3_0):  # 小数
                    data_3_1 = s('B', data_3[i2:i2 + 1])
                    data_3_3 = 0x66 - data_3_1[0] - 1
                    data_3_2 += data_3_3 * (0.01 ** (i2 + 1))
            if data_3_0 < 0:  # -200000  尾部的00不存
                data_2 = data[1:data_0]
                for i3 in range(0, data_0 - 2):  # 整数
                    data_2_1 = s('B', data_2[i3:i3 + 1])
                    data_2_3 = 0x66 - data_2_1[0] - 1
                    data_2_2 += (data_2_3) * (100 ** (data_1_1 - i3 - 1))
            data_out = (data_2_2 + data_3_2) * (-1)
        elif data_1[0] == 0x80:  # 0
            data_out = 0
        return data_out

    # 字符 char,varchar2,nchar,nvarchar2 ...
    elif col.col_type in (1, 96):
        try:
            data_out = str(data, encoding="gbk").strip()  # ascii,gbk,gb2312   .strip()
        except UnicodeDecodeError:
            data_out = 'Unicode编码溢出'
        return data_out

    # 日期时间 date
    elif col.col_type == 12:
        if len(data) != 7:
            return '0'
        else:
            data_1 = s('7B', data[0:7])
            data_out = str(((data_1[0] - 100) - 1) * 100 + data_1[1]) + '-' + str(data_1[2]) + '-' + str(
                data_1[3]) + ' ' + \
                       str(data_1[4] - 1) + ':' + str(data_1[5] - 1) + ':' + str(data_1[6] - 1)
            return data_out

    # blob,clob
    elif col.col_type == 113:
        data_out = clob_1(data, file_infos)
        return data_out
    elif col.col_type == 112:
        data_out = clob_1(data, file_infos)
        return data_out

    else:
        return 0


# 初始化页面信息
def page_init(db1, in_data):  # 初始化页面信息
    page1 = table_struct.st_page()
    page_type = s('B', in_data[0:1])  # 报这个错的，一般是 此页面数据没找到
    page1.page_type = page_type[0]
    data1 = s(db1.endian + 'I', in_data[4:8])
    pagefile = data1[0]
    file = pagefile >> 22
    page1.page_no = pagefile - 4194303 * file - file
    page1.file_no = file
    t_1 = s('B', in_data[20:21])
    t_2 = s(db1.endian + 'I', in_data[24:28])
    if db1.endian == '<':
        t_3 = s('B', in_data[36:37])
    else:
        t_3 = s('B', in_data[37:38])
    page1.page_type2 = t_1[0]
    page1.obj_id = t_2[0]
    page1.layer = t_3[0]
    blank = 8
    if file == 1:
        blank = 0
    elif file > 1:
        blank = 8
    pos_1 = 45 + (page1.layer) * 24 + blank
    sum_1 = s(db1.endian + 'BH', in_data[pos_1:(pos_1 + 3)])  # 页面中表数量和记录数量
    #  print('=========page_no:%d,obj_id:%d, tab_sum:%d, slot_sum:%d'%(page1.page_no,page1.obj_id,sum_1[0],sum_1[1]))
    page1.tab_sum = sum_1[0]
    page1.rec_sum = sum_1[1]
    for i in range(0, page1.tab_sum):  # table directory
        tab_slot1 = table_struct.tab_slot()
        slot1 = s(db1.endian + '2H', in_data[pos_1 + 13 + i * 4:pos_1 + 13 + i * 4 + 4])  # slot_off_list
        tab_slot1.tab_row_start = slot1[0]
        tab_slot1.tab_row_sum = slot1[1]
        page1.tab_slot.append(tab_slot1)
    pos_2 = pos_1 + 13 + page1.tab_sum * 4
    for i in range(0, page1.rec_sum):  # slot，row directory
        slot1 = s(db1.endian + 'H', in_data[pos_2 + i * 2:pos_2 + i * 2 + 2])  # slot_off_list
        page1.page_slot.append(slot1[0])  #
    return page1, pos_1


# 解析普通记录
def record1(db1, in_data, table, file_infos):  # 解析 compact 记录  in_data：输入页面数据,table：表结构
    page1, pos_1 = page_init(db1, in_data)  # 初始化页面,取出页面信息
    if page1.obj_id != table.tab_obj_id:
        return page1

    for i in range(0, page1.rec_sum):  # 页中的所有记录
        if page1.page_slot[i] > (db1.page_size - pos_1) or page1.page_slot[i] < (pos_1 + 16 + page1.rec_sum * 2):
            continue
        off_set = page1.page_slot[i] + pos_1 - 1
        header1 = s("3B", in_data[off_set:off_set + 3])  # 记录头
        header_0 = header1[0]  # 记录类型
        header_2 = header1[2]  # 记录列数
        # if  header_0 not in (0x3c,0x2c):   # 普通记录
        #     print(header_0)
        # if table.tab_obj_id == 18:
        #     print('slot_%d:%d, header:%s,col_sum:%d'%(i,off_set,hex(header_0),header_2))

        record1 = table_struct.st_record()  # 初始化记录结构体
        if header_0 == 0x3C:  # 删除记录
            continue
        if header_0 == 0x2c:  # 普通记录
            col_off = off_set + 3
            record1.col_sum = header_2
        elif header_0 == 0x0c:  # 普通记录, forwarding 记录
            col_off = off_set + 3 + 6
            record1.col_sum = header_2

        # 解析记录的各列数据,  行迁移，行溢出没有完成  ======================================
        for ii3 in range(0, record1.col_sum):
            len1 = s('B', in_data[col_off:col_off + 1])  # 列数据类型长度
            if len1[0] > 250 and len1[0] != 0xff:
                len1 = s(db1.endian + 'H', in_data[col_off + 1:col_off + 3])
                len2 = len1[0]
                len3 = 3  # 列长度的长度
            elif len1[0] < 250:
                len2 = len1[0]
                len3 = 1
            if len1[0] == 0xff:
                len2 = 0  # 列数据长度
                len3 = 1  # 列长度的长度
            col_data1 = in_data[col_off + len3:col_off + len3 + len2]
            if len2 == 0:
                col_data2 = 'null'
            else:
                col_data2 = data_type(col_data1, table.col[ii3], file_infos)  # 列数据解析
            #    record1.col_data1.append(col_data1)     # 放入内存
            if table.col[ii3].col_type in (112, 113):
                col_data2 = 'LOB'

            # if table.col[ii3].col_name == 'PHOTO':          # 取文件 RESUME
            #     f_1 = open(r'C:\test\test_lob\files\%s'%(record1.col_data2[1]),'wb')
            #     f_1.write(col_data2)
            #     col_data2 = 'bLOB out'
            #     f_1.close()

            record1.col_data2.append(col_data2)
            col_off = col_off + len2 + len3
        page1.record.append(record1)  # 把记录放到 页面的记录容器里,会很多
    return page1


# 解析lob字段， 大文件解析有问题
def clob_1(data, file_infos):
    len_1 = len(data)
    data_1 = s('>HHIHHQ', data[0:20])
    data_2 = s('>HBBIHHI', data[20:36])
    clob_locator = table_struct.locator()
    clob_innode = table_struct.innode()
    clob_locator.length = data_1[0]
    clob_locator.version = data_1[1]
    clob_locator.flags = data_1[2]
    clob_locator.byte_length = data_1[3]
    clob_locator.lobid_1 = data_1[4]
    clob_locator.lobid_2 = data_1[5]

    clob_innode.size = data_2[0]
    clob_innode.flag = data_2[1]
    clob_innode.full_blocks = data_2[3]
    clob_innode.bytes = data_2[4]
    clob_innode.version = str(data_2[5]) + '.' + str(data_2[6])
    clod_data = b''
    if clob_innode.full_blocks > 11:
        clob_innode.full_blocks = 11
    if clob_innode.flag == 5:
        for i in range(clob_innode.full_blocks + 1):
            data1 = s('>I', data[i * 4 + 36:(i + 1) * 4 + 36])
            pagefile = data1[0]
            file = pagefile >> 22
            page_no = pagefile - 4194303 * file - file
            file_no = file
            #      print(file_no,page_no)
            for file in file_infos:
                if file.f_no == file_no:
                    f1 = file.file
                    f1.seek(page_no * 8192)
                    data_3 = f1.read(8192)
                    data_3 = data_3[56:8188]
                    if i == clob_innode.full_blocks:
                        data_3 = data_3[0:clob_innode.bytes]
                    clod_data += data_3
                #   print(len(data_3),len(clod_data))

    return clod_data


# 解析cluster记录
def record2(db1, in_data, table, file_infos):  # 解析cluster记录   (in_data:输入页面数据,db:表结构)
    page1, pos_1 = page_init(db1, in_data)  # 初始化页面,取出页面信息
    tab1 = table;
    cluster1 = []
    for i in range(0, page1.rec_sum):  # 页中的所有记录
        if page1.page_slot[i] > (db1.page_size - pos_1) or page1.page_slot[i] < (pos_1 + 16 + page1.rec_sum * 2):
            continue
        off_set = page1.page_slot[i] + pos_1 - 1
        header1 = s("3B", in_data[off_set:off_set + 3])  # 记录头
        header_0 = header1[0]  # 记录类型
        header_2 = header1[2]  # 记录列数
        #    print('slot_%d:%d, header:%s,col_sum:%d'%(i,off_set,hex(header_0),header_2))       # 测试用

        # 解析记录的各列数据, 一般无行溢出   ======================================
        if header_0 == 0xAC:  # 簇键表记录 172
            record1 = table_struct.st_record2()  # 初始化记录结构体
            record1.col_sum = header_2
            curc = s(db1.endian + "H", in_data[off_set + 3:off_set + 5]);
            comc = s(db1.endian + "H", in_data[off_set + 5:off_set + 7])
            pk = s(">IH", in_data[off_set + 7:off_set + 13])
            pk_file = pk[0] >> 22;
            pk_page = pk[0] - 4194303 * pk_file - pk_file;
            pk_slot = pk[1]
            nk = s(">IH", in_data[off_set + 13:off_set + 19])
            nk_file = nk[0] >> 22;
            nk_page = nk[0] - 4194303 * nk_file - nk_file;
            nk_slot = nk[1]
            col_off = off_set + 19
            record1.curc = curc[0];
            record1.comc = comc[0]
            record1.pk_file = pk_file;
            record1.pk_page = pk_page;
            record1.pk_slot = pk_slot
            record1.nk_file = nk_file;
            record1.nk_page = nk_page;
            record1.nk_slot = nk_slot
        #    print('curc:%d,comc:%d,pk:%d.%d.%d,nk:%d.%d.%d'%(record1.curc,record1.comc,pk_file,pk_page,pk_slot,nk_file,nk_page,nk_slot))

        elif header_0 == 0x6C:  # 聚簇普通表记录  108
            record1 = table_struct.st_record3()  # 初始化记录结构体
            record1.col_sum = header_2
            cluster_key_idx = s("B", in_data[off_set + 3:off_set + 4])
            col_off = off_set + 4
            #    print('cluster_key_idx:%d'%(cluster_key_idx[0]))
            try:
                key = cluster1[cluster_key_idx[0]]
            except IndexError:
                print('cluster key 溢出...')
                continue
            record1.col_data1.append(key)  # 第一列的值，键列
            record1.col_data2.append(key)
        else:  # 20 记录
            continue

        # 定位到 记录的 表
        for i1 in range(0, page1.tab_sum):  # 页中表的数量，包含簇键表
            tab_row_sum = page1.tab_slot[i1].tab_row_sum
            if i >= page1.tab_slot[i1].tab_row_start and i < (page1.tab_slot[i1].tab_row_start + tab_row_sum):  #
                table = tab1[i1]
                record1.tab_no = i1
                break

        # 解析记录的各列数据
        for ii3 in range(0, record1.col_sum):
            len1 = s("B", in_data[col_off:col_off + 1])  # 列数据类型长度
            if len1[0] > 250 and len1[0] != 0xff:
                len1 = s(db1.endian + "H", in_data[col_off + 1:col_off + 3])
                len2 = len1[0]
                len3 = 3
            elif len1[0] < 250:
                len2 = len1[0]
                len3 = 1
            if len1[0] == 0xff:
                len2 = 0  # 列数据长度
                len3 = 1  # 列长度的长度

            col_data1 = in_data[col_off + len3:col_off + len3 + len2]
            if len2 == 0:
                col_data2 = 'null'
            elif len2 != 0 and header_0 == 0x6C:
                try:
                    col_data2 = data_type(col_data1, table.col[ii3 + 1], file_infos)  # 列数据解析
                except IndexError:
                    continue
            elif len2 != 0 and header_0 == 0xAC:
                col_data2 = data_type(col_data1, table.col[ii3], file_infos)  # 列数据解析
                cluster1.append(col_data2)
            #    record1.col_data1.append(col_data1)     # 放入内存
            record1.col_data2.append(col_data2)
            col_off = col_off + len2 + len3
        page1.record.append(record1)  # 把记录放到 页面的记录容器里,会很多
    return page1
