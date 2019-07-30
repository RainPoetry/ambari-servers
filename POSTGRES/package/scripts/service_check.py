from resource_management import *
from resource_management.libraries.functions.check_process_status import check_process_status

class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        check_process_status(params.postgres_pid_file)

if __name__ == "__main__":
    ServiceCheck().execute()