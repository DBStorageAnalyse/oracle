# -*- coding: utf-8 -*-
oracle check tool 
检测oracle数据文件,统计损坏的页数,打印损坏页的信息
ddd.py 是页面 校验和计算器

pyinstaller -F -w C:\Users\zsz\PycharmProjects\sqlserver\test\ui_check.py

history : ---------------------------------------------------------
oracle check tool v1.0.0  2015-2-13
检测oracle 数据文件
支持小端, 无GUI界面
输入 文件路径,起始位置(字节)

oracle check tool v1.1.0  2015-10-13
加入GUI图形界面。（pyqt5.4）
单线程
I/O: 95M/s, 无异或校验
oracle check tool v1.1.0  2015-10-14
多线程
oracle check tool v1.2.0  2015-10-17
加入HEX查看

oracle check tool v1.3.0  2016-01-06
改进校验，极大提高I/O速度
I/O: 110M/s，有异或校验

oracle check tool v1.4.0  2016-01-07
增加控制文件检测
修复bugs
进度条没有实现
oracle check tool v1.5.0  2016-05-23
修复bugs
relase
oracle check tool v1.6.0  2016-06-21
三库 联调 1
oracle check tool v1.7.0  2016-07-11
修复bugs
oracle check tool v1.8.0  2016-07-27
加入多线程界面显示