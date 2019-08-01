import os
from resource_management import *
from resource_management.core.resources.system import File, Directory
from resource_management.core.source import Template


def tracker():
    import tracker_params

    Directory(tracker_params.track_data_path,
              owner=tracker_params.fdfs_user,
              group=tracker_params.user_group,
              create_parents=True,
              mode=0750
              )

    configFile("tracker.conf", template_name="tracker.conf.j2", mode=0755)

    os.symlink("/usr/bin/fdfs_storaged","/usr/local/bin/fdfs_storaged")


def configFile(name, template_name=None, mode=None):
    import tracker_params

    File(os.path.join(tracker_params.conf_dir, name),
         content=Template(template_name),
         owner=tracker_params.fdfs_user,
         group=tracker_params.user_group,
         mode=mode
         )
