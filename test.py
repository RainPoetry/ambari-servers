#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector


# 打开数据库连接
db = mysql.connector.connect(user="root", passwd="AaBb=Cc123", database="mysql", use_unicode=True)
# db = MySQLdb.connect("localhost", "root", "AaBbCc123=", "mysql", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 更新语句

try:
    # 执行SQL语句
    cursor.execute("set global validate_password_policy=0")
    cursor.execute("set global validate_password_length=4")
    cursor.execute("alter user 'root'@'localhost' identified by 'root'")
    cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION")
    cursor.execute("FLUSH  PRIVILEGES")
    # 提交到数据库执行
    db.commit()
except Exception,err:
    # 发生错误时回滚
    db.rollback()
    print err

# 关闭数据库连接
db.close()