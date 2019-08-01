

from resource_management import *
from resource_management.libraries.script.script import Script

# server configurations
config = Script.get_config()

fdfs_user = "root"
user_group = "root"

track_data_path = config['configurations']['fdfs-tracker-env']['track_data_path']
track_port = config['configurations']['fdfs-tracker-env']['track_port']
track_http_server_port = config['configurations']['fdfs-tracker-env']['track_http_server_port']
track_store_lookup = config['configurations']['fdfs-tracker-env']['track_store_lookup']

conf_dir = "/etc/fdfs"
server_name = "fdfs_trackerd"
