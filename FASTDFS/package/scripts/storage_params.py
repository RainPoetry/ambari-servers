

from resource_management import *
from resource_management.libraries.script.script import Script

# server configurations
config = Script.get_config()

fdfs_user = "root"
user_group = "root"

storage_base_path = config['configurations']['fdfs-storage-env']['storage_base_path']
storage_data_path = config['configurations']['fdfs-storage-env']['storage_data_path']
storage_group_name = config['configurations']['fdfs-storage-env']['storage_group_name']
storage_port = config['configurations']['fdfs-storage-env']['storage_port']
storage_http_server_port = config['configurations']['fdfs-storage-env']['storage_http_server_port']

track_port = config['configurations']['fdfs-tracker-env']['track_port']

tracker_hosts = config['clusterHostInfo']['fastdfs_tracker_hosts']

conf_dir = "/etc/fdfs"
server_name = "fdfs_storaged"