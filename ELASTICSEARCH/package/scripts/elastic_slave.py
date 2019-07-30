"""
Elastic service script.

"""

from resource_management import *
import signal
import sys
import os
from os.path import isfile
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.exceptions import ComponentIsNotRunning

from slave  import slave


class elastic_slave(Script):
    def install(self, env):
        self.install_packages(env)
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        slave()

    def stop(self, env):
        import params
        env.set_params(params)
        self.deal("stop")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        self.deal("start")

    def status(self, env):
        import params
        env.set_params(params)
        self.deal("status")

    def deal(self,action):
        import params
        daemon_name = params.server_name
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
    elastic_slave().execute()


