# -*- coding: utf-8 -*-
oracle 数据文件 碎片扫描/拼接
支持9i,10g,11g,12c，支持大小端
扫描结果(页面位置和信息)存储在sqlite数据库中，可按扇区步进扫描。

oar_scan.py 是碎片扫描
link1.py 是碎片物理拼接

空页文件号为0的情况是什么原因 ？？？
file>3的是

拼碎片： 逻辑拼接

cd C:\Users\zsz\PycharmProjects\sqlserver\test
pyinstaller -F -w C:\Users\zsz\PycharmProjects\sqlserver\test\ui_scan.py
======== history ============================================
oracle scan tool v1.0  2015-2-13
oracle 数据文件碎片扫描工具
支持小端, 无GUI界面
python3.4+Qt5.4
oracle scan tool v1.1  2015-8-25
支持9i,10g,11g,12c，支持大小端，无GUI.(因为有跨平台需要，先不做UI)
扫描结果(页面位置和信息)存储在sqlite数据库中
可按扇区步进扫描
oracle scan tool v1.2  2016-01-17
加入界面
优化速度，修复bug
oracle scan tool v1.3  2016-01-31
完善功能，修复bugs
oracle scan tool v1.4.0  2016-03-05
加入数据页中记录列数的获取(file>3)
oracle scan tool v1.5.2  2016-05-07
去除了temp文件里的页面
优化扫描碎片，修复bugs
oracle scan tool v1.6.0  2016-05-18
优化界面功能
加入导出功能
加入注册验证
oracle scan tool v1.6.2  2016-06-07
修复bugs
优化界面
加入log输出
oracle scan tool v1.7.0  2016-06-21
3库联调
oracle scan tool v1.8.0  2016-07-05
完善导出模块
oracle scan tool v1.8.2  2016-07-06
修复link_1中的bug
修复结束偏移的设置
oracle scan tool v1.8.6  2016-07-14
修复bugs
加入link_3
oracle scan tool v1.8.8  2016-07-21
完善link_3(页号连续，片段文件号相同，scn相近筛选)
oracle scan tool v1.9.0  2016-07-25
优化link_2
加入多线程，界面加入进度显示
多线程 速度好像慢些
oracle scan tool v1.9.2  2016-07-26
优化界面，拼接


需要加入 加密压缩ora_scan.db

-------- test ----------------------------------------------
280G 的img , 扫描用时：1小时, 磁盘I/O: 40M/s
500Gd img ,  2h（xor不做）, 71.5M/s       2015.6.25
2T 的硬盘，有400G的数据库页，扫描 50-60m/s（无论是否加xor）,
sqlite 中ora_page表的每行30B，每1G的dbf对应4m的db, 400m/100G=4G/1T
50m/s=3G/min=180G/h=1T/5.7h   磁盘I/O: 45-50M/s
============================================================
数据库 自主武器系统
MSSQL :
1. 拼接工具
2. 文件解析
3. 检测工具（mdf文件检测）
4. 日志解析工具
5. bak文件工具（bak扫描提取，bak解析，mdf提取）
6. 删除恢复工具

ORACLE:
1. 拼接工具
2. 文件解析
3. 检测工具
4. ASM工具（ASM解析，dbf导出）
5. 控制文件解析工具
6. 删除恢复工具

MYSQL :
1. 拼接工具
2. 文件解析
3. 检测工具
4. frm文件工具（扫描，解析）
5. dump文件工具（暂无）


=============================================================

