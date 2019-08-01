import os
from resource_management import *
from resource_management.core.resources.system import File, Directory
from resource_management.core.source import Template


def storage():
    import storage_params

    Directory(storage_params.storage_base_path,
              owner=storage_params.fdfs_user,
              group=storage_params.user_group,
              create_parents=True,
              mode=0755
              )

    Directory(storage_params.storage_data_path,
              owner=storage_params.fdfs_user,
              group=storage_params.user_group,
              create_parents=True,
              mode=0755
              )

    configFile("storage.conf", template_name="storage.conf.j2", mode=0755)


def configFile(name, template_name=None, mode=None):
    import storage_params

    File(os.path.join(storage_params.conf_dir, name),
         content=Template(template_name),
         owner=storage_params.fdfs_user,
         group=storage_params.user_group,
         mode=mode
         )
