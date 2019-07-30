from resource_management.libraries.functions import format
from resource_management.libraries.script.script import Script

config = Script.get_config()

postgres_pid_dir = "/var/lib/pgsql/11/data"
postgres_pid_file = postgres_pid_dir+"/postmaster.pid"