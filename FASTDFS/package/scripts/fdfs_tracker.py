"""
Elastic master file
"""

from resource_management import *
import signal
import sys
import os
from os.path import isfile
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.resources.packaging import Package
from tracker import tracker

class fdfs_tracker(Script):
    def install(self, env):
        config = self.get_config()
        agent_stack_retry_on_unavailability = bool(config['ambariLevelParams']['agent_stack_retry_on_unavailability'])
        agent_stack_retry_count = int(config['ambariLevelParams']['agent_stack_retry_count'])
        Package("fastdfs.x86_64",
                retry_on_repo_unavailability=agent_stack_retry_on_unavailability,
                retry_count=agent_stack_retry_count)
        self.configure(env)

    def configure(self, env):
        import tracker_params
        env.set_params(tracker_params)
        tracker()

    def stop(self, env):
        import tracker_params
        env.set_params(tracker_params)
        self.deal("stop")


    def start(self, env):
        import tracker_params
        env.set_params(tracker_params)
        self.deal("start")

    def status(self, env):
        import tracker_params
        env.set_params(tracker_params)
        self.deal("status")

    def deal(self,action):
        import tracker_params
        daemon_name = tracker_params.server_name
        cmd = ('service', daemon_name, action)
        if action == 'status':
            try:
                Execute(cmd)
            except Fail:
                raise ComponentIsNotRunning()
        elif action == 'stop':
            Execute(cmd,
                    logoutput = True,
                    sudo = True
                    )
        elif action == 'start':
            Execute(cmd,
                    logoutput = True,
                    sudo = True
                    )

if __name__ == "__main__":
    fdfs_tracker().execute()


