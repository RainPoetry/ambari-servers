#!/usr/bin/env python
"""
Elasticsearch Params configurations
"""

from resource_management import *
from resource_management.libraries.script.script import Script

# server configurations
config = Script.get_config()

elastic_home = '/etc/elasticsearch/'
elastic_bin = '/usr/share/elasticsearch/bin/'
server_name = "elasticsearch"


conf_dir = "/etc/elasticsearch"
elastic_user = config['configurations']['elastic-env']['elastic_user']
user_group =config['configurations']['elastic-env']['user_group']
log_dir = config['configurations']['elastic-env']['elastic_log_dir']
pid_dir = '/var/run/elasticsearch'
pid_file = '/var/run/elasticsearch/elasticsearch.pid'
hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
elastic_env_sh_template = config['configurations']['elastic-env']['content']

cluster_name = config['configurations']['elastic-site']['cluster_name']
path_data = config['configurations']['elastic-site']['path_data']
path_log = config['configurations']['elastic-site']['path_log']
nodes = config['configurations']['elastic-site']['nodes']
http_port =  config['configurations']['elastic-site']['http_port']