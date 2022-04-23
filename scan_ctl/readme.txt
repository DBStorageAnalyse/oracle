# -*- coding: utf-8 -*-
oracle scan tool
oracle 控制文件 工具
大，小端，无GUI
扫描结果(页面位置和信息)存储在 ./aa.db 中
按扇区步进扫描。
扫描时，磁盘I/O: 40M/s

ora_scan(f_name,start,endian,db_name)



history =============================================================================
oracle scan tool v1.0.0  2015-02-13
oracle 控制文件碎片扫描工具
oracle scan tool v1.2.0  2016-07-03
需要准确性优化
oracle scan tool v1.3.0  2016-07-06
修复link_1中的bug
修复结束偏移的设置


-------test--------------------------------
280G 的img , 扫描用时：1小时（xor不做）



