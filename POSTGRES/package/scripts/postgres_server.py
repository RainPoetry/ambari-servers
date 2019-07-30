import sys, os
from resource_management import Script
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.core.logger import Logger
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.core.exceptions import ComponentIsNotRunning
from postgres import postgres


class Server(Script):
    def install(self, env):
        self.install_packages(env)
        self.configure(env)

    def configure(self, env):
        import params
        env.set_params(params)
        postgres()

    def start(self, env):
        import params
        env.set_params(params)
        daemon_cmd = format('{params.postgres_bin}/pg_ctl -D {params.postgres_data} -l {params.postgres_log_file} start')
        Execute(daemon_cmd,
                user=params.postgres_user
        )


    def stop(self, env):
        import params
        env.set_params(params)
        daemon_cmd = format('kill -INT `head -1 {params.postgres_pid_file}`')
        try:
            Execute(daemon_cmd,
                    user=params.postgres_user)
        except:
            show_logs(params.postgres_log_file, params.postgres_user)
            raise
        # File(params.postgres_pid_file,
        #      action = "delete"
        #      )

    def status(self, env):
        import status_params
        env.set_params(status_params)
        pid_file = status_params.postgres_pid_file
        if not pid_file or not os.path.isfile(pid_file):
            raise ComponentIsNotRunning()
        # check_process_status(pid_file)
        # print "status"

    def get_pid_files(self):
        import params
        return [params.postgres_pid_file]

if __name__ == "__main__":
    Server().execute()