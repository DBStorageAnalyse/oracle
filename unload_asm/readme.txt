# -*- coding: utf-8 -*-
oracle ASM 解析
解析ASM磁盘，获取文件

开发平台：win8.1 + PyCharm Community Edition4.5 + python3.4 + pyqt5.3

history : ==============================================
v1.0  2015-8-13
支持大小端, GUI界面
64位程序，不支持32位系统(xp/2003)

v1.2  2015-9-8
优化功能
加入导出文件功能
v1.2.6  2015-9-12
修复bug,优化功能
v1.2.7  2015-9-13
修复bug,优化功能
加入元数据文件的显示和导出

v1.2.8  2015-9-17
重新架构asm.py ：asm 函数做成类，
改为多进程导出文件。
多线程还有点问题，不能同时导出多个文件。数据会错乱
加入选中文件导出
导出的I/O: 40m/s
v1.2.9  2015-10-6
改进选中文件导出
修复bug
v1.3.1  2015-10-7
磁盘信息 按磁盘组和磁盘号排序
支持缺盘解析
导出的 I/O ： 40M/s
v1.3.2  2015-10-8
优化 文件别名，导出准确度
导出的 I/O ： 40M/s
v1.3.4  2015-10-10
加入log输出和异常处理
改进高级信息
改进导出,提升I/O性能
v1.3.6  2015-10-11
修复bugs
v1.3.7  2015-10-12
修复bugs
v1.3.8  2015-10-17
修复bugs
加载disk0.5分钟内，解析5分钟内。
v1.3.9 2015-10-18
修复bugs(导出，解析)
v1.4.0 2015-10-19
修复bug (导出修复11.2以后的变化AU)
10T->200M内存  ？？？

v1.4.2 2015-10-22
改进导出算法（性能和准确度）
v1.4.3 2015-10-24
改进导出算法（性能和准确度）
v1.4.4 2015-10-28
改进导出算法（性能和准确度）
v1.4.6 2015-10-29
加入导出文件指针信息到db
（不导出文件，解析和导出信息在10分钟内）
i/o: 40M/s=2.4G/min=150G/h
v1.5.0 2016-05-20
加入注册验证
v1.6.0 2016-06-21
3库联调


加入进度显示
文件table 排序功能
加入停止进程，，

处理 内存占用高,导出I/O慢

检测损坏 时 只须注释掉 导出的 read()和write()，seek()

==================================================== test ==============================================
大，小端，测过实战过
需要 AMS 磁盘镜像的前1G
磁盘数>150,磁盘组总容量>80T,导出 单文件>300G,
10.1/10.2/11.1/11.2/

要先解析文件目录(文件1)，然后解析 磁盘目录元文件(文件2),获取到磁盘文件目录，再解析别名目录,文件6
注：文件列表应该按 文件6的， 不按 文件1 的。不然会不全。

release: 发布为exe
C:\Python34\Scripts> cxfreeze C:\Users\zsz\PycharmProjects\sqlserver\test\ui_asm.py --target-dir=C:\Users\zsz\PycharmProjects\sqlserver\test\tt --base-name=C:\Python34\Lib\site-packages\cx_Freeze\bases\Win32GUI.exe
pyinstaller -F C:\Users\zsz\PycharmProjects\sqlserver\test\ui_asm.py        # -w


