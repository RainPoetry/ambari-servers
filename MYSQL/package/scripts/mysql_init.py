from resource_management import *
#from yaml_config import yaml_config
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.logger import Logger
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.functions.format import format
from resource_management.core.source import InlineTemplate, Template
import os
import sys
from resource_management.core import sudo
import re


def mysql_init():
    import params

    data = sudo.read_file(params.mysql_log_file)
    initPasswd = readPassword(data)
    Execute(format("mysqladmin -uroot -p'{initPasswd}' password {params.mysql_temp_passwd}"))
    updateMysql(params.mysql_temp_passwd,params.mysql_password)


def readPassword(data):
    matchObj = re.findall('temporary password is generated for root@localhost:(.*)', data, re.I)
    if len(matchObj) == 0:
        raise Exception("can't find the init password")
    passwd = matchObj[-1].strip()
    return passwd

def updateMysql(temp_passwd,passwd):
    import mysql.connector

    db = mysql.connector.connect(user="root", passwd=temp_passwd, database="mysql", use_unicode=True)
    # db = MySQLdb.connect("localhost", "root", "AaBbCc123=", "mysql", charset='utf8' )

    cursor = db.cursor()

    sql ="""
    set global validate_password_policy=0;
    set global validate_password_length=4;
    alter user 'root'@'localhost' identified by '{passwd}';
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '{passwd}' WITH GRANT OPTION;
    FLUSH  PRIVILEGES;
    """.format(passwd=passwd)
    try:
        cursor.execute("set global validate_password_policy=0")
        cursor.execute("set global validate_password_length=4")
        cursor.execute(format("alter user 'root'@'localhost' identified by '{passwd}'"))
        cursor.execute(format("GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '{passwd}' WITH GRANT OPTION"))
        cursor.execute("FLUSH  PRIVILEGES")
        db.commit()
    except Exception,err:
        db.rollback()
        print err
        raise Exception(err)

    db.close()



