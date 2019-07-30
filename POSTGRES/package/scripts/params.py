from resource_management.libraries.functions import format
from resource_management.libraries.script.script import Script

import json

config = Script.get_config()

postgres_home = '/usr/pgsql-11'
postgres_bin = postgres_home + "/bin"
postgres_data = "/var/lib/pgsql/11/data"
postgres_data_hba = postgres_data+"/pg_hba.conf"
postgres_data_conf = postgres_data + "/postgresql.conf"

postgres_user = config['configurations']['postgres-env']['postgres_user']
user_group = config['configurations']['postgres-env']['user_group']
postgres_log_dir = config['configurations']['postgres-env']['postgres_log_dir']
port = config['configurations']['postgres-env']['port']
pid_file_dir = config['configurations']['postgres-env']['pid_file_dir']


postgres_log_file = postgres_log_dir + "/server.log"
postgres_pid_dir = postgres_data
postgres_pid_file = postgres_pid_dir+"/postmaster.pid"
