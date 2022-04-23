#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 定义 各种结构体

class File_Info():
    def __init__(self):
        self.endian = ''  # 平台软件的字节顺序(大小端),0:小端,1:大端
        self.hard = 0  # 用于标识的magic数,4k:0x82,8k:0xa2,16k:0xc2
        self.f_name = ''  # 文件路径
        self.f_no = 0  # 文件号
        self.file = 0
        self.f_type = ''  # 文件类型
        self.blk_size = 8192  # 文件的块/页 大小 (B)
        self.blk_sum = 0  # 文件的块/页 总数
        self.DBID = 0  # 数据库ID
        self.SID = ''  # SID,库名
        self.ts_id = 0  # 表空间ID
        self.ts_name = ''  # 表空间名
        self.version = ''  # 版本
        self.big_ts = 0  # 是否是大文件
        self.os = ''  # OS信息
        self.boot = 0  # 启动页


class st_db:  # 数据库
    def __init__(self):
        self.db_id = 0  # 数据库 ID
        self.db_name = ''  # 数据库名
        self.version = ''  # 数据库版本
        self.page_size = 0  # 页面大小,固定为8192字节
        self.endian = ''  # 大小端. 0小端,1大端
        self.os = ''  # OS信息
        self.tab0 = []  # 表 bootstrap$,obj$
        self.tab1 = []  # 表C_OBJ#
        self.tab2 = []  # 表C_USER#


class st_table:  # 表
    def __init__(self):
        self.db_id = 0  # 数据库 ID
        #   self.tab_type = 0         # 表的类型
        self.tab_obj_id = 0  # 表的 object_id
        self.bobj = 0  # 父对象号
        self.tab_no = 0  # 簇表中的编号
        self.tab_name = ''  # 表名  #有的表只有object_id没有表名
        self.owner = 0  # 所属用户ID
        self.owner_name = ''  # 所属用户名
        self.col_sum = 0  # 表的总列数
        self.col = []  # 列信息,表结构中的
        self.col_1 = []  # 强猜的列结构信息
        self.pkey_have = 0  # 是否有主键
        self.ts = 0  # 表空间号
        self.file_no = 0  # 表数据起始页号
        self.page_no = 0  # 表数据起始页号
        self.rowcnt = 0  # 表的记录数量
        self.extcnt = 0  # 表的区数量
        self.blkcnt = 0  # 表的页面数量
        self.sql = ''
        self.ext = []  # 表的区指针
        self.indexes = []  # 表的索引


class st_index:  # 索引
    def __init__(self):
        self.obj_id = 0  # 表的 object_id
        self.bobj = 0  # 父对象号
        self.ind_name = ''  # 表名  #有的表只有object_id没有表名
        self.owner = 0  # 所属用户ID
        self.ts = 0  # 表空间号
        self.file_no = 0  # 表数据起始页号
        self.page_no = 0  # 表数据起始页号
        self.col_sum = 0  # 索引的总列数
        self.col = []  # 列信息,结构中的
        self.ext = []  # 索引的区指针


class st_ext:  # 区位图
    def __init__(self):
        self.dba_off_f = 0  # 页偏移的文件号
        self.dba_off_b = 0  # 页偏移的块号
        self.dba_sum = 0  # 页数


class st_column:  # 列
    def __init__(self):
        self.tab_obj_id = 0  # 表的object_id
        self.col_id = 0  # 列id
        self.col_name = ''  # 列名
        self.col_type = 0  # 列的数据类型
        self.col_type_name = ''  # 列的数据类型名称
        self.col_len = 0  # 列长度
        self.prec = 0  # 精度
        self.scale = 0  # 小数位数
        self.collationid = 0  # 排序规则编号
        self.seed = 0  # 自增种子.  标识种子+标识增量
        self.def_data = 'NULL'  # 默认值
        self.nullable_is = 0  # 是否可为空
        self.varlen_is = 0  # 是否是变长
        self.pkey_is = 0  # 是否是主键


class st_page:  # 页面
    def __init__(self):
        self.page_no = 0  # 页面编号，从0编号
        self.file_no = 1  # 文件号， 从1编号
        self.page_type = 0  # 页面类型：数据页，IAM页，索引页
        self.page_type2 = 0  # 页面类型：数据页，IAM页，索引页
        self.obj_id = 0  # object_id
        self.layer = 0  # itl事务槽的数量
        self.tab_sum = 0  # 页面中表数量
        self.rec_sum = 0  # 页面中记录数量,即slot数量
        self.flagBits = 0  # 页面校验标志
        self.tab_slot = []  # table directory
        self.page_slot = []  # slot，row directory
        self.record = []  # 页面中的记录 结构


class tab_slot:  # table directory
    def __init__(self):
        self.tab_row_start = 0  # 表的起始记录号
        self.tab_row_sun = 0  # 表的记录数量


class st_record:  # 数据记录
    def __init__(self):
        # self.rec_off = 0         # 记录的起始偏移
        self.flag = 0  # 记录类型
        self.col_sum = 0  # 记录的列数，不一定是表结构的总列数
        self.col_len = 0  # 列数据长度
        self.col_data1 = []  # 记录的解析前列数据
        self.col_data2 = []  # 记录的解析后列数据


class st_record2:  # 簇键表记录
    def __init__(self):
        # self.rec_off = 0         # 记录的起始偏移
        self.curc = 0
        self.comc = 0
        self.pk_file = 0
        self.pk_page = 0
        self.pk_slot = 0
        self.nk_file = 0
        self.nk_page = 0
        self.nk_slot = 0
        self.flag = 0  # 记录类型
        self.col_sum = 0  # 记录的列数，不一定是表结构的总列数
        self.col_len = 0  # 列数据长度
        self.tab_no = 0  # 记录的表编号
        self.col_data1 = []  # 记录的解析前列数据
        self.col_data2 = []  # 记录的解析后列数据


class st_record3:  # 簇普通表数据记录
    def __init__(self):
        # self.rec_off = 0         # 记录的起始偏移
        self.cluster_key_idx = 0  # 记录类型
        self.col_sum = 0  # 记录的列数，不一定是表结构的总列数
        self.col_len = 0  # 列数据长度
        self.tab_no = 0  # 记录的表编号
        self.col_data1 = []  # 记录的 解析前 列数据
        self.col_data2 = []  # 记录的 解析后 列数据


class locator:
    def __init__(self):
        self.length = 0  # 记录类型
        self.version = 0  # 记录的列数，不一定是表结构的总列数
        self.flags = 0
        self.byte_length = 0  # 列数据长度
        self.lobid_1 = 0  # 记录的表编号
        self.lobid_2 = 0  # 记录的表编号


class innode:
    def __init__(self):
        self.size = 0  # 记录类型
        self.flag = 0
        self.full_blocks = 0
        self.bytes = 0
        self.version = ''
