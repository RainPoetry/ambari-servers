import sys, os
from resource_management import Script
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.resources.service import Service
from resource_management.core.logger import Logger
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.exceptions import ComponentIsNotRunning
from mysql_init import mysql_init



class mysql_server(Script):
    def install(self, env):
        self.install_packages(env)
        self.start(env)
        mysql_init()

    def configure(self, env):
        import params
        env.set_params(params)

    def start(self, env):
        import params
        env.set_params(params)
        cmd = ('service', params.service_name, "start")
        Execute(cmd,
                logoutput = True,
                sudo = True
                )

    def stop(self, env):
        import params
        env.set_params(params)
        cmd = ('service', params.service_name, "stop")
        Execute(cmd,
                logoutput = True,
                sudo = True
                )

    def status(self, env):
        import params
        env.set_params(params)
        pid_file = params.mysql_pid_file
        check_process_status(pid_file)

    def get_pid_files(self):
        import params
        return [params.mysql_pid_file]


if __name__ == "__main__":
    mysql_server().execute()