#!/usr/bin/env python
"""
elasticsearch service params.

"""

from resource_management import *
import sys
from copy import deepcopy
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.format import format

def elastic():
    import params

    params.path_data = params.path_data.replace('"','')
    data_path = params.path_data.replace(' ','').split(',')
    data_path[:]=[x.replace('"','') for x in data_path]
    
    directories = [params.log_dir, params.pid_dir, params.conf_dir]
    directories = directories+data_path;
    
    Directory(directories,
              owner=params.elastic_user,
              group=params.elastic_user,
              create_parents = True,
              mode=0750
          )
    
    File(format("{conf_dir}/elastic-env.sh"),
          owner=params.elastic_user,
          group=params.elastic_user,
          content=InlineTemplate(params.elastic_env_sh_template)
     )

    configurations = params.config['configurations']['elastic-site']

    File(format("{conf_dir}/elasticsearch.yml"),
       content=Template(
                        "elasticsearch.master.yaml.j2",
                        configurations = configurations),
       owner=params.elastic_user,
       group=params.elastic_user
    )
    
    File(format("/etc/sysconfig/elasticsearch"),
       content=Template(
                        "elasticsearch.sysconfig.j2",
                        configurations = configurations),
       owner=params.elastic_user,
       group=params.elastic_user,
       mode=0750
    )