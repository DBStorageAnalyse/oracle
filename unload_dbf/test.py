# -*- coding: utf-8 -*-
import cx_Oracle

print(cx_Oracle.buildtime)  # 验证cx_Oracle 是否安装导入成功
db = cx_Oracle.connect('system', 'oracle', '10.3.9.50:1521/orcl')  # 建立连接，3 个参数分开写
print(db.version)  # 验证 Oracle 是否连接成功

cursor = db.cursor()
cursor.execute("select * from tab")

cursor.close()
db.commit()
db.close()
