#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 读取数据库文件进行解析, 主函数 模块
import struct, time
import init

s = struct.unpack


class Unload_DB():
    def __init__(self):  # 解析函数
        super(Unload_DB, self).__init__()
        self.files = []

    # 文件信息
    def file_init(self, fn):
        self.files = []
        for f_name in fn:  # 每个文件头信息
            f = open(f_name, 'rb')
            data = f.read(32)
            file_info = init.file_blk_0(data)
            f.seek(file_info.blk_size)
            data = f.read(file_info.blk_size)
            file_info = init.file_blk_1(data)
            file_info.f_name = f_name
            file_info.file = f
            self.files.append(file_info)
        return self.files

    # 解析控制文件
    def unload_db(self, file_infos):
        file_info = file_infos[0]
        files = init.unload_ctl(file_info)

        return files
