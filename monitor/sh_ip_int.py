from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from user_login import user_login
from nornir.core.filter import F
import ipdb

user_login()
nr = InitNornir(config_file="config.yaml")
task1 = nr.filter(F(groups__contains='IOS'))


def version_task(task):
    r = task.run(netmiko_send_command,
                 command_string=" show ip int br | inc down ")
    task.host['facts'] = r.result


sh_version = task1.run(task=version_task)
print_result(sh_version)

