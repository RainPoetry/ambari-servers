from resource_management import *
#from yaml_config import yaml_config
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.logger import Logger
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.functions.format import format
from resource_management.core.source import InlineTemplate, Template
import os
import sys


def postgres():
    import params

    if os.path.exists(params.postgres_data):
        pass
    else:
        Directory(params.postgres_log_dir,
                  owner=params.postgres_user,
                  create_parents = True,
                  group=params.user_group,
                  mode=0750
                  )

        # Directory(params.postgres_pid_dir,
        #           owner=params.postgres_user,
        #           create_parents = True,
        #           group=params.user_group,
        #           mode=0755,
        #           )
        daemon_cmd = format("{params.postgres_bin}/postgresql-11-setup initdb")
        try:
            Execute(daemon_cmd)
        except:
            show_logs(params.postgres_log_file, params.postgres_user)
            raise
        configFile("pg_hba.conf",template_name="pg_hba.conf.j2")
        configFile("postgresql.conf",template_name="postgresql.conf.j2")



def configFile(name, template_name=None, mode=None):
    import params

    File(os.path.join(params.postgres_data, name),
         content=Template(template_name),
         owner=params.postgres_user,
         group=params.user_group,
         mode=mode
         )