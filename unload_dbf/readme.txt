# -*- coding: utf-8 -*-
oracle 数据文件 解析工具
1. 字典模式/system 存在
先解析 出几个重要系统表， 然后通过这几个系统表的数据 来解析全部。

2. 非字典模式/system不存在
解析所有段，按object_id解析， 自动猜解字段。

cd /d C:\Python34\Scripts
cxfreeze C:\Users\zsz\PycharmProjects\sqlserver\test\ui_unload.py --target-dir=C:\Users\zsz\PycharmProjects\sqlserver\test\tt
cd /d C:\Users\zsz\PycharmProjects\sqlserver\test

pyinstaller -F -w C:\zsz\ML\code\database\PycharmProjects\oracle\unload_dbf\ui_unload.py
打包的exe好大啊
对cx_Oracle的支持有问题
=============================================================================
history:
V1.0.0      2015-6-20
测试版本，无界面
V1.1.0      2015-10-20
完善记录解析，系统表解析
下一版需要解析 空间管理，多文件
V1.2.0      2015-11-11
加入界面
解析 空间管理，多文件
V1.3.0     2016-01-03
三库 联调 1
system.dbf解析太慢
V1.4.0     2016-04-01
V1.5.0     2016-05-20
加入注册验证
V1.5.2     2016-05-28
加入BLOB,CLOB的解析（不全）
加入索引的解析显示
V1.6.0     2016-06-15
完善界面和功能(关于)
V1.7.0     2016-06-17
完善界面和功能
V1.8.0     2016-06-21
三库 联调 2
V1.8.6     2016-07-08
修复bug，number的解析
完善功能
V1.9.0     2016-07-27
加入多线程界面显示


加强准确度(记录解析，记录数量)

----------------------------------------------------------------------------
# create table tab_info(id integer primary key,tab_obj_id,BOBJ,TAB_NO,tab_type,tab_name,col_sum) # bobj是父对象ID：分区表是主表ID,普通表即表ID
# create table col_info(id integer primary key,tab_obj_id,col_id,col_name,col_data_type,col_len)
# insert into tab_info(tab_obj_id,BOBJ,TAB_NO,tab_type,tab_name,col_sum) values(86,2,8,0,'subcoltype$',8)
# insert into col_info(tab_obj_id,col_id,col_name,col_data_type,col_len) values(1,3,'sql_test',2,0)

解析普通表：obj$ ======= page_no: 240 =======
解析聚簇表：C_OBJ# ======= page_no: 144 =======
解析慢


