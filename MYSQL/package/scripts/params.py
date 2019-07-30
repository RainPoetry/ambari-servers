from resource_management.libraries.functions import format
from resource_management.libraries.script.script import Script

import json

config = Script.get_config()

mysql_user = "root"
user_group = "root"

mysql_temp_passwd = "AaBb=Cc123"
mysql_password = config['configurations']['mysql-env']['password']

mysql_log_dir = "/var/log"
mysql_log_file = "/var/log/mysqld.log"
mysql_my_file = "/etc/my.cnf"
mysql_data_dir = "/var/lib/mysql"
mysql_pid_file = "/var/run/mysqld/mysqld.pid"

service_name= "mysqld.service"


